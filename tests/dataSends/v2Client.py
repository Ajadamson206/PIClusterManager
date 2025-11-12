#!/usr/bin/env python3

# Version 2: (2, light, humidity, moisture, air_temp, soil_temp)
# (uint32, f64, f64, f64, f64, f64)

import socket
import struct

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(("localhost", 5000))

raw_data = struct.pack('<Iddddd', 2, 1.23, 2.4, 3.5, 4.6, 5.7)

clientsocket.send(raw_data)
clientsocket.close()