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
    
    except :
        print("Unable to create file register.txt")
        print("Use the following command for help: register --help")

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

    if args.file:
        pass
    elif args.mac_address and args.name and args.power_source and args.plotid:
        pass
    else:
        pass

if __name__ == "__main__":
    main()