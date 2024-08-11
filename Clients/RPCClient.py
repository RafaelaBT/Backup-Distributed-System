# Essential Libraries
import socket, json

# Buffer size
SIZE = 65536

# RPC Client class
class RPCClient:
    # Client constructor
    def __init__(self, host:str='127.0.0.1', port:int=65432) -> None:
        # Client socket and info
        self.__sock = None
        self.address = (host, port)

    # Client connection
    def connect(self):
        try:
            # Create socket
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Try to connect with Manager
            #print("> Client status: Trying to connect with Manager...")
            self.__sock.connect(self.address)
            #print("> Client status: Connection accepted.")

        except EOFError:
            raise Exception('> Client status: not able to connect.')
    
    # Verify connection
    def isConnected(self):
        try:
            #print("\n> Client status: Connection test.")
            self.string('Connection test.')
            #print("> Client status: Client is connected.")
            return True
    
        except:
            #print("> Client status: Unavailable server.")
            return False
    
    # Close connection
    def disconnect(self):
        try:
            # Close socket
            self.__sock.close()
            #print("\n> Client status: Connection closed.")
        except:
            pass

    # Send file to backup system
    def sendFile(self, path:str, filename:str):
        # Get principal server
        addr = self.getServer()

        try:
            # Conect to server
            client = RPCClient(addr[0], addr[1])
            client.connect()

            # Send filename
            client.sendFilename(filename)

            # Send file
            with open (path + filename, 'rb') as file:
                while True:
                    chunk = file.read(SIZE)
                    if not chunk:
                        break
                    # Send file by chunks
                    client.__sock.sendall(chunk)
            # Send End Of File
            client.__sock.sendall(b'EOF')

            # Get server response
            response = json.loads(client.__sock.recv(SIZE).decode())
            #print(f"\n> Client status: {response}")

            # Disconect
            client.disconnect()

            return True
        except:
            #print("\n> Client status: Unable to send file.")
            return False

    # Client stub
    def __getattr__(self, __name:str):
        def execute(*args, **kwargs):
            # Send parameters
            self.__sock.sendall(json.dumps((__name, args, kwargs)).encode())
            
            # Get response
            response = json.loads(self.__sock.recv(SIZE).decode())
            return response
        return execute

    # Delete connection
    def __del__(self):
        try:
            self.__sock.close()
        except:
            pass