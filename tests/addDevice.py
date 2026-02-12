#!/usr/bin/env python3

IP=""
MAC=""
DEVICE_ID=1
PLOTID=1

import sqlite3

class DBConnect:
    def __init__(self, db_loc):
        self.db_loc = db_loc

        try:
            self.conn = sqlite3.connect(self.db_loc, timeout=30, isolation_level=None)
            self.cursor = self.conn.cursor()

            # Enable WAL mode (persistent)
            self.cursor.execute("PRAGMA journal_mode=WAL;")
            
            self.cursor.execute("PRAGMA synchronous=NORMAL;")
            self.cursor.execute("PRAGMA foreign_keys=ON;")

            self.conn.execute("PRAGMA busy_timeout=30000;")  # 30 seconds

        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}\nExiting...")
            exit(1)

    def addDevice(self, deviceID: int, plotID: int, ip: str, mac: str):
        self.cursor.execute(
            "INSERT INTO plots VALUES (?, ?);",
            (plotID, "Test")
        )
        self.conn.commit()
    
        self.cursor.execute(
            "INSERT INTO networkDevices VALUES (?, ?, ?, ?, ?, ?, ?);",
            (deviceID, mac, ip, "Test Device", "Wall Power", 100.0, plotID)
        )
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()

