#!/usr/bin/env python3

# Version 1: (1, battery_life) 
# (uint32, f64)

import socket
import struct
import json

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(("192.168.50.1", 6000))

dict = {
    "light": 20,
    "moisture": 50,
    "soil_temp": 22,
    "humidity": 43,
    "air_temp": 50,
    "battery": 30
}

clientsocket.send(bytes(json.dumps(dict), 'utf-8'))
clientsocket.close()