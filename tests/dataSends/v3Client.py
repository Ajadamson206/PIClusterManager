#!/usr/bin/env python3

# Send Data that should raise a Unicode Error 

import socket
import struct

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(("localhost", 5000))

raw_data = struct.pack('<I6d', 3, 1.23, 2.4, 3.5, 4.6, 5.7, 6.8)

clientsocket.send(raw_data)
clientsocket.close()