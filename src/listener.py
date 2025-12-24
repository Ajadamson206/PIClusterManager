
import socket
from typing import List
from dbconnect import DBConnect
from parser import parseData
import netifaces
from pathlib import Path
from logger import globalLogger


class Listener:
    def __init__(self, port: int, db_loc: str, host: str, adapter: str):
        self.port = port
        self.db_loc = db_loc
        self.host = host
        self.adapter = adapter

        # Get SQL Connection
        try:
            self.db = DBConnect(self.db_loc)
            self.db.verifyTables()
        except FileExistsError as e:
            globalLogger.logCriticalError(f"Unable to Open/Create Database: {e}")
            exit(1)
        
        # Initialize listener socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.db.getCountOfDevices() + 3)  # Allow some extra connections

    def main_loop(self):
        # Main listening loop to handle incoming data
        while True:
            connection, address = self.socket.accept()

            # None of the packets should be greater than 1024 bytes
            buffer = connection.recv(1024)
            numBytes = len(buffer)

            # Indicates that the client has disconnected
            if numBytes == 0:
                pass
            
            else:
                # Parse the data received
                print(f"Received data from {address}: {buffer}")
                parsed_data = parseData(buffer, address)
                print(f"Parsed data: {parsed_data}")

    def getDHCPAddresses(self, file="/var/lib/misc/dnsmasq.leases") -> List[str] | List[None]:
        picos = []
        path = Path(file)

        if not path.exists():
            globalLogger.logError(f"Cannot find dnsmasq leases: {file}")
            return picos
        
        try:
            with path.open() as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) < 4:
                        continue

                    picos.append(parts[2])

        except:
            globalLogger.logError(f"Unable to open dnsmasq leases: {file}")
            return picos

        if len(picos) == 0:
            globalLogger.logWarning("No DHCP leases found")

        return picos

    # Send request messages to the picos in the network
    def requestMessages(self):
        # Get hosts on subnet (Iterate through list to prevent network overcrowding)
        picos = self.getDHCPAddresses()

        """
            All picos should be listening on port 9000 UDP
            Send a message on that port containing this IP address and port num
        """

        ip = netifaces.ifaddresses(self.adapter).get(netifaces.AF_INET)
        if not ip:
            globalLogger.logCriticalError(f"The specified interface '{self.adapter}' does not exist or does not have an ip. Exiting")
            exit(1)

        broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        for pico in picos:
            broadcast.sendto(ip[0]['addr'] + str(self.port), (pico, 9000))