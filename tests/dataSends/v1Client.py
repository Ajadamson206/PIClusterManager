#!/usr/bin/env python3

# Version 1: (1, battery_life) 
# (uint32, f64)

import socket
import struct

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(("localhost", 5000))

raw_data = struct.pack('<Id', 1, 1.23)

clientsocket.send(raw_data)
clientsocket.close()