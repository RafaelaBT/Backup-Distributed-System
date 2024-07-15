# Essential Libraries
import socket
import json

# Buffer size
SIZE = 1024

# RPC Client class
class RPCClient:
    # Client constructor
    def __init__(self, host:str='127.0.0.1', port:int=65433) -> None:
        self.__sock = None
        self.__address = (host, port)

    # Client connection
    def connect(self):
        try:
            # Create socket
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Try to connect with Server
            print("> Client status: Trying to connect with Server...")
            self.__sock.connect(self.__address)
            print("> Client status: Connection accepted.")

        except EOFError:
            raise Exception('> Client status: not able to connect.')
        
    def isConnected(self):
        try:
            print("\n> Client status: Connection test.")
            self.string('Connection test.')
            print("> Client status: Client is connected.")
            return True
    
        except:
            print("> Client status: Unavailable server.")
            return False
    
    # Disconnect client
    def disconnect(self):
        try:
            # Close socket
            self.__sock.close()
            print("\n> Client status: Connection closed.")
        except:
            pass

    def sendFile(self, path:str, filename:str):
        try:
            self.sendFilename(filename)

            with open (path + filename, 'rb') as file:
                while True:
                    chunk = file.read(SIZE)
                    if not chunk:
                        break
                    self.__sock.sendall(chunk)
            self.__sock.sendall(b'EOF')

            response = json.loads(self.__sock.recv(SIZE).decode())
            print(f"\n> Client status: {response}")
            return True
        
        except:
            print("\n> Client status: Unable to send file.")
            return False

    def __getattr__(self, __name:str):
        def execute(*args, **kwargs):
            self.__sock.sendall(json.dumps((__name, args, kwargs)).encode())

            response = json.loads(self.__sock.recv(SIZE).decode())

            return response
        return execute

    def __del__(self):
        try:
            self.__sock.close()
        except:
            pass