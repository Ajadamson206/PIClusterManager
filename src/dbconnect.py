import sqlite3

class DBConnect:
    def __init__(self, db_loc):
        self.db_loc = db_loc

        try:
            self.conn = sqlite3.connect(self.db_loc)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise FileExistsError("Database connection failed at " + db_loc + "\nCheck if the path is correct and writable.")

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
                print(f"Error creating table {table_name}: {e}")

    def getCountOfDevices(self) -> int:
        try:
            self.cursor.execute("SELECT COUNT(*) FROM networkDevices;")
            return int(self.cursor.fetchone()[0])
        except sqlite3.Error as e:
            print(f"Error fetching device count: {e}")
            return 0

    def close(self):
        if self.conn:
            self.conn.close()