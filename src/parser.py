import ctypes
from typing import Tuple
import json


def parseData(data: bytes, address: Tuple[str, int]) -> dict:
    """
    Data is now going to be using JSON

    {
    light: level
    moisture: level
    soil_temp: level
    humidity: level
    air_temp: Level
    battery: level
    }
    
    """
    
    print(data)
    data_loaded = json.loads(data)
    print(data_loaded)
    return data_loaded