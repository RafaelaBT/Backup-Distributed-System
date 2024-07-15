# Import modules
import sys, os
path = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.append(path + '../')
from RPC.RPCServer import RPCServer

# Create server
server = RPCServer()

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