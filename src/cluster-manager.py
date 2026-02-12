#!/usr/bin/env python3

import argparse
import json
from logger import globalLogger

from listener import Listener

# Cluster Manager Made to be ran on the Central Raspberry PI 4


"""

    Each pico will monitor light, soil temp, soil moisture.
    
    Temperature, air humidity will be monitored by a central sensor.

    0. Read configuration file for settings
        db_loc: {file_path}     # File path to the location of the SQL file
        port_num: {1-65535}     # Port number to listen on for Pico Data

    1. Connect to SQL and verify tables
        SQL:
            Connect to the databse located at {db_loc}
            If no database is found create it from scratch
        
        Tables:
            plotData(Plot_ID, datetime, light, humidity, moisture, air_temp, soil_temp)
            networkDevices(Device_ID, MAC Address, Device Name, Solar/Battery, Battery Level, Plot_ID, IsOnline)
            averages(Plot_ID, average_type {Daily, Weekly, Monthly}, light, humidity, moisture, air_temp, soil_temp)
            
    2. Listen on Port {port_num} for data from the Picos

    3. Parse the Data Sent by the Pico
        ->  Couple different formats of data packet starts off with an 8-bit 'Version'
            which explains what data was sent
                - 1: (battery_life)
                - 2: (light, humidity, moisture, air_temp, soil_temp)
                - 3: (battery_life, light, humidity, moisture, air_temp, soil_temp)
        ->  Looks something like this: 
                (1/2/3, ...)

    4. Convert the parsed data into an SQL Query for the respective table
        ->  Pull the Device_ID and Plot_ID via the device's MAC address
                - select Plot_ID, Device_ID from plotInfo where MAC = ?
        ->  Update battery life in networkDevices
                - 
        ->  

    5. Validate and Send the query

"""

def main():
    # Parse configuration file
    parser = argparse.ArgumentParser(
                        prog='Cluster-Manager',
                        description="Pi Cluster Manager for Raspberry Pi 4")
    parser.add_argument('-c','--config', type=str, default="/etc/garden/garden-cluster-config.json", help='Path to the configuration file')
    args = parser.parse_args()

    # Load configuration file
    with open(args.config, 'r') as f:
        config = json.load(f)

    db_loc = config["db_loc"]
    port_num = config["port_num"]
    host = config["host"]
    adapter = config["adapter"]
    time_loc = config["time_state"]

    # Determine the log level
    if "loglevel" in config and 0 <= config["loglevel"] <= 2:
        loglevel = config["loglevel"]
       
        if loglevel == 1:
            globalLogger.hideDebug()
        elif loglevel == 2:
            globalLogger.hideWarning()

        globalLogger.logDebug(f"loglevel: {loglevel}")
    else:
        globalLogger.hideDebug()
        globalLogger.logWarning("Unknown loglevel: defaulting to 1")

    # Use Listener to handle incoming data
    listener = Listener(port_num, db_loc, host, adapter, time_loc)
    listener.main_loop()

if __name__ == "__main__":
    main()
