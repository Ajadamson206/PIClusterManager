import sqlite3
from logger import globalLogger

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
                    datetime TEXT,
                    light REAL,
                    humidity REAL,
                    moisture REAL,
                    air_temp REAL,
                    soil_temp REAL
                );
            """,
            "networkDevices": """
                CREATE TABLE IF NOT EXISTS networkDevices (
                    Device_ID INTEGER PRIMARY KEY,
                    MAC_Address TEXT UNIQUE,
                    Device_Name TEXT,
                    Power_Source TEXT,
                    Battery_Level REAL,
                    Plot_ID INTEGER,
                    IsOnline INTEGER
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
                globalLogger.logError(f"Error creating table {table_name}: {e}")

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
                "SELECT Device_ID FROM networkDevices WHERE Device_ID = ?;",
                (ip_address,)
            )
            result = self.cursor.fetchone()
            if result:
                return int(result[0])
            else:
                return -1
        except sqlite3.Error as e:
            globalLogger.logError(f"Error finding device ID for {ip_address}: {e}")
            return -1

    def updateIPaddress(self, mac_address: str, ip_address: str) -> bool:
        try:
            self.cursor.execute(
                "UPDATE networkDevices SET Device_ID = ? WHERE MAC_Address = ?;",
                (ip_address, mac_address)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            globalLogger.logError(f"Error updating IP address for {mac_address}: {e}")
            return False

    def updateBatteryLife(self, ip_address: str, battery_life: float) -> bool:
        try:
            # Find the deviceID by IP
            deviceId = self.findDeviceID(ip_address)
            if deviceId == -1:
                print(f"Device with IP {ip_address} not found.")
                return

            self.cursor.execute(
                "UPDATE networkDevices SET Battery_Level = ? WHERE Device_ID = ?;",
                (battery_life, deviceId)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            globalLogger.logError(f"Error updating battery life for {ip_address}: {e}")
            return False

    def close(self):
        if self.conn:
            self.conn.close()