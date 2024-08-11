# Import modules
import sys, os
path = os.path.dirname(os.path.abspath(__file__)) + '/Backups/'
os.makedirs(path, exist_ok=True)

def getSize(path):
    size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            size += os.path.getsize(fp)
    return size

sys.path.append(path + '../../')
from RPCServer import RPCServer

IP = '127.0.0.1'
PORT = 65433
CAPACITY = getSize(path)

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