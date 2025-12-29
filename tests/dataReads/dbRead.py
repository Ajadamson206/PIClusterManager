#!/usr/bin/env python3
import sqlite3

db_loc = "build/sql.db"

conn = sqlite3.connect(db_loc)
cursor = conn.cursor()

# Read Network Devices
cursor.execute("SELECT * FROM networkDevices;")
print(cursor.fetchall())

# Read Plot_data
cursor.execute("SELECT * FROM plotData;")
print(cursor.fetchall())

