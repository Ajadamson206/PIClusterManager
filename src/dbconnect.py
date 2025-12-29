import sqlite3
from logger import globalLogger
from datetime import datetime

class DBConnect:
    def __init__(self, db_loc):
        self.db_loc = db_loc

        try:
            self.conn = sqlite3.connect(self.db_loc)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            globalLogger.logCriticalError(f"Error connecting to database: {e}\nExiting...")
            exit(1)

    def verifyTables(self):
        # Verify and create tables if they do not exist
        table_creation_queries = {
            "plotData": """
                CREATE TABLE IF NOT EXISTS plotData (
                    Plot_ID INTEGER,
                    time DATETIME,
                    light REAL,
                    humidity REAL,
                    moisture REAL,
                    air_temp REAL,
                    soil_temp REAL
                );
            """,
            "networkDevices": """
                CREATE TABLE IF NOT EXISTS networkDevices (
                    Device_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    MAC_Address TEXT UNIQUE,
                    IP_Address TEXT,
                    Device_Name TEXT,
                    Power_Source TEXT,
                    Battery_Level REAL,
                    Plot_ID INTEGER,
                    IsOnline BOOLEAN
                );
            """,
            "averages": """
                CREATE TABLE IF NOT EXISTS averages (
                    Plot_ID INTEGER,
                    average_type TEXT,
                    light REAL,
                    humidity REAL,
                    moisture REAL,
                    air_temp REAL,
                    soil_temp REAL
                );
            """
        }

        for table_name, query in table_creation_queries.items():
            try:
                self.cursor.execute(query)
                self.conn.commit()
            except sqlite3.Error as e:
                globalLogger.logCriticalError(f"Error creating table {table_name}: {e}")
                exit(1)

        if not self.checkIfDeviceExists(int(0)):

            # Device_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            # MAC_Address TEXT UNIQUE,
            # IP_Address TEXT,
            # Device_Name TEXT,
            # Power_Source TEXT,
            # Battery_Level REAL,
            # Plot_ID INTEGER,
            # IsOnline BOOLEAN

            self.cursor.execute(
                "INSERT INTO networkDevices VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                (0, "FF:FF:FF:FF:FF:FF", "127.0.0.1", "Server", "Wall Power", 100.0, 0, True)
            )
            self.conn.commit()

    def checkIfDeviceExists(self, deviceID: int) -> bool:
        try:
            self.cursor.execute(
                "SELECT COUNT(*) FROM networkDevices WHERE Device_ID = ?;",
                (deviceID,)
            )
            return int(self.cursor.fetchone()[0]) == 1
        except sqlite3.Error as e:
            globalLogger.logError(f"Error Checking if Device {deviceID} exists: {e}")
            return False

    def getCountOfDevices(self) -> int:
        try:
            self.cursor.execute("SELECT COUNT(*) FROM networkDevices;")
            return int(self.cursor.fetchone()[0])
        except sqlite3.Error as e:
            globalLogger.logError(f"Error fetching device count: {e}")
            return 0

    def findDeviceID(self, ip_address: str) -> int:
        try:
            self.cursor.execute(
                "SELECT Device_ID FROM networkDevices WHERE IP_Address = ?;",
                (ip_address,)
            )
            result = self.cursor.fetchone()
            if result:
                return int(result[0])
            else:
                globalLogger.logWarning(f"No Device ID found for {ip_address}: {e}")
                return -1
        except sqlite3.Error as e:
            globalLogger.logError(f"Error finding device ID for {ip_address}: {e}")
            return -1

    def updateIPaddress(self, mac_address: str, ip_address: str) -> bool:
        try:
            self.cursor.execute(
                "UPDATE networkDevices SET IP_Address = ? WHERE MAC_Address = ?;",
                (ip_address, mac_address)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            globalLogger.logError(f"Error updating IP address for {mac_address}: {e}")
            return False

    def updateBatteryLife(self, deviceID: int, battery_life: float) -> bool:
        try:
            self.cursor.execute(
                "UPDATE networkDevices SET Battery_Level = ? WHERE Device_ID = ?;",
                (battery_life, deviceID)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            globalLogger.logError(f"Error updating battery life for device {deviceID}: {e}")
            return False

    def getDevicePlot(self, deviceID: int) -> int:
        try:
            # Extract Device PlotID
            self.cursor.execute("SELECT Plot_ID FROM networkDevices WHERE Device_ID = ?;",
            (deviceID,))
            return int(self.cursor.fetchone()[0])
        except sqlite3.Error as e:
            globalLogger.logError(f"Error fetching device count: {e}")
            return 0

    def addGardenData(self, ip_address: str, data: dict) -> bool:
        try:
            # Get Device ID
            deviceID = self.findDeviceID(ip_address)
            if deviceID == -1:
                return False

            # {
            # light: level
            # moisture: level
            # soil_temp: level
            # humidity: level
            # air_temp: Level
            # battery: level
            # }

            if "battery" in data:
                print("Updating Battery")
                self.updateBatteryLife(deviceID, float(data["battery"]))

            # time DATETIME,
            # light REAL,
            # humidity REAL,
            # moisture REAL,
            # air_temp REAL,
            # soil_temp REAL           

            self.cursor.execute(
                "INSERT INTO plotData VALUES (?, ?, ?, ?, ?, ?, ?);",
                (self.getDevicePlot(deviceID), datetime.now().isoformat(timespec="seconds"), data["light"], data["humidity"], data["moisture"], data["air_temp"], data["soil_temp"])
            )
            self.conn.commit()

            return True
        except sqlite3.Error as e:
            globalLogger.logError(f"Error adding new garden data for {ip_address}: {e}")
            return False

    def close(self):
        if self.conn:
            self.conn.close()