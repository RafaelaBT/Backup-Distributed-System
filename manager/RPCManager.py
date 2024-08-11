# Essential Libraries
import inspect, socket, json, copy
from threading import Thread

# Buffer size
SIZE = 65536

# RPC Manager class
class RPCManager:
    # Manager constructor
    def __init__(self, host:str='127.0.0.1', port:int=65432) -> None:
        # Manager info
        self.host = host
        self.port = port
        self.addr = (host, port)
        self._methods = {}
        self._servers = {}

    # Methods register
    def registerMethod(self, function) -> None:
        try:
            # Register method
            self._methods.update({function.__name__:function})
        except:
            raise Exception('\n> Manager status: A non function object has been passed into RPCManager.registerMethod(self, function)')

    # Instance's methods register
    def registerInstace(self, instance=None) -> None:
        try:
            # Register instance's methods
            for functionName, function in inspect.getmembers(instance, predicate=inspect.ismethod):
                if not functionName.startswith('__'): # private
                    self._methods.update({functionName: function})
        except:
            raise Exception('\n> Manager status: A non class object has been passed into RPCManager.registerInstance(self, instance)')
    
    # Return Addr as a key from servers dictionary
    def getKey(self, addr:str):
        return str(addr[0])+":"+str(addr[1])
    
    # Show ON servers
    def showServers(self) -> None:
        print("> Servers ON:")
        for key, value in self._servers.items():
            print(f"\t{key}: {value}")
    
    # Add server to servers dictionary
    def serverRegister(self, addr:tuple, capacity:int):
        name = self.getKey(addr)
        self._servers[name] = {'capacity':capacity}
        print(f"\n> Manager status: server {name} is ON.")
        self.showServers()
        return True
    
    # Remove server from servers dictionary
    def delServer(self, addr:tuple) -> None:
        try:
            name = self.getKey(addr)
            del self._servers[name]
            print(f"\n> Manager status: Server {name} is OFF.")
            self.showServers()
        except KeyError as e:
            raise Exception(f"\nManager status: couldn't remove {name}.")
    
    # Choose server from servers dictionary
    def chooseServer(self, addr):
        # Create a copy from servers dictionary
        cdict = copy.deepcopy(self._servers)

        # Remove server addr
        if addr != None:
            del cdict[self.getKey(addr)]

        # Choose server by capacity (bytes)
        addr = min(cdict, key=lambda k: cdict[k]['capacity']).split(':')
        print(f"\n> Manager status: {addr} is the chosen server.")
        ip = addr[0]
        port = int(addr[1])
        return (ip, port)
    
    # Update server capacity
    def updateCapacity(self, addr:tuple, capacity:int):
        name = self.getKey(addr)
        self._servers[name]['capacity'] = capacity
        print(f"\n> Manager status: Server capacity {name} updated to {self._servers[name]}.")
        self.showServers()
        return True
    
    # Get servers dictionary size
    def getSize(self):
        return len(self._servers)
        
    # Thread body
    def __handle__(self, conn:socket.socket, addr:tuple) -> None:
        print(f"\n> Manager Status: Connected with {addr[0]}:{addr[1]}")

        while True:
            try:
                # Receive data
                functionName, args, kwargs = json.loads(conn.recv(SIZE).decode())

            except:
                print(f"\n> Manager status: {addr[0]}:{addr[1]} disconnected.")
                break

            # Show data
            print(f"\n> Data from {addr[0]}:{addr[1]}: {functionName}{args}")

            try:
                # Create response
                response = self._methods[functionName](*args, **kwargs)
            except Exception as e:
                print(f"\n> Manager status: Sending error...")
                conn.sendall(json.dumps(str(e)).encode())
            else:
                # Send response
                print(f"\n> Manager Status: Returning data...")
                conn.sendall(json.dumps(response).encode())
                print("> Manager Status: Data sent successfully!")

        # Close connection
        conn.close()
        print(f"\n> Manager status: Connection closed.")

    # Manager runner
    def run(self) -> None:
        # All threads array
        threads = []

        # Create a socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Associate the socket with the manager info
            sock.bind(self.addr)

            # Ennable the manager accept connections
            sock.listen()
            print("> Manager Status: ON.")

            try:
                while True:
                    # Accept a connection
                    conn, addr = sock.accept()

                    # Create and start a thread
                    thread = Thread(target=self.__handle__, args=[conn, addr])
                    thread.start()

                    # Append thread
                    threads.append(thread)
            except KeyboardInterrupt:
                print("\n> Manager closed unexpectedly.") # Ctrl + C
            finally:
                if sock:
                    sock.close()   # Close socket
                for thread in threads:
                    thread.join()    # Wait thread finish