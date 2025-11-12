
import socket
from dbconnect import DBConnect


class Listener:
    def __init__(self, port: int, db_loc: str, host: str):
        self.port = port
        self.db_loc = db_loc
        self.host = host
    
        # Get SQL Connection
        try:
            self.db = DBConnect(self.db_loc)
            self.db.verifyTables()
        except FileExistsError as e:
            print(f"Unable to Open/Create Database: {e}")
            exit(1)
        
        # Initialize listener socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.db.getCountOfDevices() + 3)  # Allow some extra connections

    def main_loop(self):
        # Main listening loop to handle incoming data
        while True:
            connection, address = self.socket.accept()
            buffer = connection.recv(512)

            if len(buffer) > 0:
                # Parse the data received

                print(f"Received data from {address}: {buffer}")
