#!/usr/bin/env python3

# Send an improper formatted JSON output

import socket
import json

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(("localhost", 5000))

dict = """{
    "light": 20,
    "moisture": 30,
    "soil_temp": 40,
    "humidity": 50,
    "air_temp": 60
    "battery": 70
"""
clientsocket.send(bytes(dict, 'utf-8'))
clientsocket.close()