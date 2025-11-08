# Cluster Manager Made to be ran on the Central Raspberry PI 4

"""
    0. Read configuration file for settings
        db_loc: {file_path}     # File path to the location of the SQL file
        port_num: {1-65535}     # Port number to listen on for Pico Data

    1. Listen on Port 20000 for data from the Picos

    2. Write the data to an SQL server (SQLite3)
        -> Data is formatted like this (light, humidity, moisture, air temp, soil temp)



"""