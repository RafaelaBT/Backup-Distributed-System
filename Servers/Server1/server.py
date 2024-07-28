# Import modules
import sys, os
path = os.path.dirname(os.path.abspath(__file__)) + '/Backups/'
os.makedirs(path, exist_ok=True)

content = os.listdir(path)
files = [f for f in content if os.path.isfile(os.path.join(path, f))]

sys.path.append(path + '../../')
from RPCServer import RPCServer

IP = '127.0.0.1'
PORT = 65433
CAPACITY = len(files)

# Create server
server = RPCServer(IP, PORT, CAPACITY)

# Return string
def string(s:str):
    return s

def sendPath():
    return path

# Register methods
server.registerMethod(string)
server.registerMethod(sendPath)

# Run server
server.run()