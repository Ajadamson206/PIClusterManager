import ctypes
from typing import Tuple


def parseData(data: bytes, address: Tuple[str, int]) -> dict:
    """
    Parse the incoming data packet from the Pico.

    Data packet formats:
        Version 1: (1, battery_life)
        Version 2: (2, light, humidity, moisture, air_temp, soil_temp)
        Version 3: (3, battery_life, light, humidity, moisture, air_temp, soil_temp)
    """
    if len(data) < 4:
        print(f"Data packet from ({address}) is too short to contain version information.")
        return {}
    
    # Version is a 32-bit integer
    version = int(data[0]<<24 | data[1]<<16 | data[2]<<8 | data[3])

    if version == 1:
        return version1(data)
    elif version == 2:
        return version2(data)
    elif version == 3:
        return version3(data)
    else:
        print(f"Unrecognized version ({version}) from ({address}).")
        return {}


def version1(data: bytes) -> dict:
    pass

def version2(data: bytes) -> dict:
    pass

def version3(data: bytes) -> dict:
    pass