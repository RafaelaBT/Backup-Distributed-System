# Essential libraries
import sys, os

# Create backup folder
path = os.path.dirname(os.path.abspath(__file__)) + '/Backups/'
os.makedirs(path, exist_ok=True)

# Get files size in bytes
def getSize(path):
    size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            size += os.path.getsize(fp)
    return size

# Import modules
sys.path.append(path + '../../')
from RPCServer import RPCServer

# Server info
IP = '127.0.0.1'
PORT = 65435
CAPACITY = getSize(path)

# Create server
server = RPCServer(IP, PORT, CAPACITY)

# Return string
def string(s:str):
    return s

# Send server path
def sendPath():
    return path

# Register methods
server.registerMethod(string)
server.registerMethod(sendPath)

# Run server
server.run()