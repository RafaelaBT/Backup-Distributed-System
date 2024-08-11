# Essential Libraries
import inspect, socket, json, os
from threading import Thread

# Buffer size
SIZE = 65536

# RPC Server class
class RPCServer:
    # Server constructor
    def __init__(self, host:str, port:int, capacity:int, mngHost:str='127.0.0.1', mngPort:int = 65432) -> None:
        self.__sock = None
        self.managerAddr = (mngHost, mngPort)

        self.host = host
        self.port = port
        self.addr = (host, port)
        self.capacity = capacity

        self._methods = {}

    # Methods register
    def registerMethod(self, function) -> None:
        try:
            # Register method
            self._methods.update({function.__name__:function})
        except:
            raise Exception('\n> Server status: A non function object has been passed into RPCServer.registerMethod(self, function)')

    # Instance's methods register
    def registerInstace(self, instance=None) -> None:
        try:
            # Register instance's methods
            for functionName, function in inspect.getmembers(instance, predicate=inspect.ismethod):
                if not functionName.startswith('__'): # private
                    self._methods.update({functionName: function})
        except:
            raise Exception('\n> Server status: A non class object has been passed into RPCServer.registerInstance(self, instance)')
        
    def __connect__(self):
        try:
            # Create socket
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Try to connect with Manager
            print("> Server status: Trying to connect with Manager...")
            self.__sock.connect(self.managerAddr)
            print("> Server status: Connection accepted.")

            if self.addServer(self.addr, self.capacity):
                print("\n> Server status: Server registered.")

        except EOFError:
            raise Exception('> Server status: not able to connect.')
        
    def __getattr__(self, __name:str):
        def execute(*args, **kwargs):
            self.__sock.sendall(json.dumps((__name, args, kwargs)).encode())

            response = json.loads(self.__sock.recv(SIZE).decode())

            return response
        return execute

    # Disconnect server
    def disconnect(self):
        try:
            # Close socket
            self.removeServer(self.addr)
            self.__sock.close()
            print("\n> Server status: Connection with Manager closed.")
        except:
            pass
    
    def __del__(self):
        try:
            self.__sock.close()
        except:
            pass

    def backup(self, addr:tuple, path:str, filename:str):
        try:
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(">\n Server status: Trying to connect with Server...")
            sock.connect((addr[0], addr[1]))

            print("> Server status: Connection accepted.")
            sock.sendall(json.dumps(('sendFilename', [filename], "backup")).encode())

            with open (path + filename, 'rb') as file:
                while True:
                    chunk = file.read(SIZE)
                    if not chunk:
                        break
                    sock.sendall(chunk)
            sock.sendall(b'EOF')

            response = json.loads(sock.recv(SIZE).decode())
            print(f"\n> Server status: {response}")
            sock.close()

        except EOFError:
            raise Exception('> Client status: not able to connect.')

    # Thread body
    def __handle__(self, conn:socket.socket, addr:tuple) -> None:
        print(f"\n> Server Status: Connected with {addr[0]}:{addr[1]}")

        while True:
            try:
                # Receive data
                functionName, args, kwargs = json.loads(conn.recv(SIZE).decode())

            except:
                print(f"\n> Server status: Client {addr[0]}:{addr[1]} disconnected.")
                break

            # Show data
            print(f"\n> Data from {addr[0]}:{addr[1]}: {args}")

            if functionName == 'sendFilename':
                conn.sendall(json.dumps('Filename received.').encode())

                try: 
                    path = self._methods['sendPath']()
                    filename = args[0]
                    
                    with open(path + filename, 'wb') as file:
                        while True:
                            chunk = conn.recv(SIZE)
                            if chunk.endswith(b'EOF'):
                                file.write(chunk[:-3])
                                break
                            file.write(chunk)

                except Exception as e:
                    print(f"\n> Server status: Sending error...")
                    conn.sendall(json.dumps(str(e)).encode())
                else:
                    self.capacity += os.path.getsize(path + filename)
                    self.updateServer(self.addr, self.capacity)

                    # Send response
                    print(f"\n> Server Status: Returning data...")
                    conn.sendall(json.dumps('File received successfully!').encode())
                    print("> Server Status: Data sent successfully!")

                if kwargs != "backup":
                    if self.getQuantity() > 1:
                        server = self.getServer(self.addr)
                        self.backup(server, path, filename)
            else:
                try:
                    # Create response
                    response = self._methods[functionName](*args, **kwargs)
                except Exception as e:
                    print(f"\n> Server status: Sending error...")
                    conn.sendall(json.dumps(str(e)).encode())
                else:
                    # Send response
                    print(f"\n> Server Status: Returning data...")
                    conn.sendall(json.dumps(response).encode())
                    print("> Server Status: Data sent successfully!")

        # Close connection
        conn.close()
        print(f"\n> Server status: Connection closed.")

    # Server runner
    def run(self) -> None:
        self.__connect__()

        threads = []

        # Create a socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Associate the socket with the server info
            sock.bind(self.addr)

            # Ennable the server accept connections
            sock.listen()
            print("\n> Server Status: ON.")

            try:
                while True:
                    # Accept a connection
                    conn, addr = sock.accept()

                    # Create and start a thread
                    thread2 = Thread(target=self.__handle__, args=[conn, addr])
                    thread2.start()

                    # Append thread
                    threads.append(thread2)
            except KeyboardInterrupt:
                print("\n> Server closed unexpectedly.") # Ctrl + C
            finally:
                if sock:
                    sock.close()   # Close socket
                for thread in threads:
                    thread.join()    # Wait thread finish'''

        self.disconnect()