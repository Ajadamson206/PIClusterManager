# A local API is going to be used for writes since simulatenous reads can cause issues for sqlite

# Used only on localhost only

# API Things:
#   1. Register new pico devices into the database
#   2. Register new plots into the database
#

"""
CREATE TABLE IF NOT EXISTS plotData (
    Plot_ID INTEGER,
    time DATETIME,
    light REAL,
    humidity REAL,
    moisture REAL,
    air_temp REAL,
    soil_temp REAL
);
CREATE TABLE IF NOT EXISTS networkDevices (
    Device_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    MAC_Address TEXT UNIQUE,
    IP_Address TEXT,
    Device_Name TEXT,
    Power_Source TEXT,
    Battery_Level REAL,
    Plot_ID INTEGER,
);
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

# API Format For Pico:
# {
#   "register": "netDevice",
#   "MAC_Address": "",
#   "IP_Address": "",
#   "Device_Name": "Device",
#   "Power_Source": "Solar",
#   "Battery_Level": 100.0,
#   "Plot_ID": 2
# }

# Output
# { "Success": "True" }
# { "Failure": "Error Message" }

from dbconnect import DBConnect
from logger import globalLogger

class AdminPanel:
    def __init__(self, db: DBConnect):
        self.db = db

    def registerDevice(self, data: dict):
        pass

    def registerPlot(self, data: dict):
        pass

    def adminMessage(self, data: dict):
        globalLogger.logDebug("Calling Admin Panel")

        if "register" in data:
            if data["register"] == "netDevice":
                self.registerDevice(data)
            elif data["register"] == "plot":
                self.registerPlot(data)
            else:
                globalLogger.logWarning(f"Unknown register type: {data['register']}")
