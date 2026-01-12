#!/usr/bin/env python3

# Register a new device in the database and for MAC Filtering

# cluster manager already needs to be running

# Run special file and insert a file path with these contents
#   mac_address=TEXT
#   device_name=TEXT
#   power_source=TEXT
#   plotid=INTEGER
# Or run the script with these flags
#   -m      {MAC_ADDRESS}
#   -n      {Device_name}
#   -ps     {Power Source}
#   -pid    {Plot ID}

# This will automatically update both the MAC Address Filter and the Device Database

import argparse
import os
import socket
import json

def noArguments():
    # Tell user that they did not enter any arguments
    print("No arguments were added to the function call.")
    print("Creating empty file called: register.txt")

    # Create new file in the current spot called register.txt
    try:
        with open("register.txt", "w") as file:
            file.write("mac_address=\ndevice_name=\npower_source=\nplotid=")
        print("Successfully created file")
        print("Modify register.txt with your settings than execute: sudo register -f register.txt")
        print("Or use the following command for help: register --help")
    
    except:
        print("Unable to create file register.txt")
        print("Use the following command for help: register --help")

def settingsParse(filePath: str) -> dict:
    settings = ["mac_address=", "device_name=", "power_source=", "plotid="]

    retDict = {}

    try:
        with open(filePath, 'r') as file:
            for line in file.readlines():
                foundSetting = False
                for setting in settings:
                    if line.startswith(setting):
                        foundSetting = True
                        line = line.strip(setting)

                        if len(line) == 0:
                            print(f"No value set for {setting}. Exiting")
                            exit(1)

                        settings.pop(setting)
                        setting = setting.replace('=', '')

                        retDict.update({setting: line})
                        foundSetting = True
                        break
                
                if not foundSetting:
                    print(f"Unknown setting: {line}")
                    print("Ignoring...")
        
        if len(setting) != 0:
            print(f"Missing lines: {settings}")
            exit(1)

        return retDict

    except:
        print("Unable to read from file. Exiting")
        exit(1)

def updateMACFilter(macAddress: str):
    hostapdAcceptPath = "/etc/hostapd/hostapd.accept"

    try:
        with open(hostapdAcceptPath, 'a') as file:
            file.write(f"{macAddress}\n")
        print("Successfully updated MAC Address Filter")
    except:
        print("Unable to update MAC Address Filter")
        exit(1)

def main():
    parser = argparse.ArgumentParser(
                        prog='Pico Registerer',
                        description='Register a new device to be added to the Pico Cluster')
    
    parser.add_argument('-f', '--file', help="Import options from a file")
    parser.add_argument('-m', '--mac-address', help='MAC Address of the New Device')
    parser.add_argument('-n', '--name', help='What the name of the device should be')
    parser.add_argument('-ps', '--power-source', help='How the device is getting power')
    parser.add_argument('-pid', '--plotid', help='ID Number of the Assigned Plot')

    args = parser.parse_args()

    # Check if the user inputted no arguments
    noArgs = True
    for arg in args._get_kwargs():
        if arg[1]:
            noArgs = False
            break
    
    if noArgs:
        noArguments()
        return

    # Check for sudo privileges
    if os.geteuid() != 0:
        print("This command needs root privilleges to run. Execute it again with sudo")
        return

    # Parse the Settings depending on the passed parameters
    if args.file:
        deviceOptions = settingsParse()
    elif args.mac_address and args.name and args.power_source and args.plotid:
        deviceOptions = {}
        deviceOptions.update({"mac_address": args.mac_address})
        deviceOptions.update({"device_name": args.name})
        deviceOptions.update({"power_source": args.power_source})
        deviceOptions.update({"plotid": args.plotid})
    else:
        noArguments()
        return

    # Update MAC Address Filter
    updateMACFilter(deviceOptions['mac_address'])

    # Update the DB
    deviceOptions.update({"register": "netDevice"})

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(("localhost", 5000))

    clientsocket.send(bytes(json.dumps(deviceOptions), 'utf-8'))
    clientsocket.close()

if __name__ == "__main__":
    main()