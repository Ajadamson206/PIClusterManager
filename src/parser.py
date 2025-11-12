import ctypes
import struct
from typing import Tuple
import numpy as np


def parseData(data: bytes, address: Tuple[str, int]) -> Tuple[int, tuple]:
    """
    Parse the incoming data packet from the Pico.

    Data packet formats:
        Version 1: (1, battery_life)
        Version 2: (2, light, humidity, moisture, air_temp, soil_temp)
        Version 3: (3, battery_life, light, humidity, moisture, air_temp, soil_temp)
    """
    if len(data) < 4:
        print(f"Data packet from ({address}) is too short to contain version information.")
        return (0, ())
    
    version, = struct.unpack_from('<I', data, 0)
    print("Header:", version)


    if version == 1:
        return (1, version1(data[4:]))
    elif version == 2:
        return (2, version2(data[4:]))
    elif version == 3:
        return (3, version3(data[4:]))
    else:
        print(f"Unrecognized version ({version}) from ({address}).")
        return (0, ())


def version1(data: bytes) -> tuple:
    if len(data) != 8:
        print("Invalid data length for version 1.")
        return ()
 
    parsedData = struct.unpack_from('<d', data, 0)
 
    print("Values:", parsedData)
    
    return parsedData

def version2(data: bytes) -> tuple:
    if len(data) != 40:
        print("Invalid data length for version 2.")
        return ()
    
    parsedData = struct.unpack_from('<5d', data, 0)

    print("Values:", parsedData)

    return parsedData

def version3(data: bytes) -> tuple:
    if len(data) != 48:
        print("Invalid data length for version 3.")
        return ()
    
    parsedData = struct.unpack_from('<6d', data, 0)

    print("Values:", parsedData)
    
    return parsedData