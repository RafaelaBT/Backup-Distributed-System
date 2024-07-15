# Import modules
import sys, os
path = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.append(path + '../')
from RPC.RPCManager import RPCManager

# Create server
manager = RPCManager()

# Return string
def string(s:str):
    return s

def serverRegister(addr:tuple):
    manager._servers.append(addr)
    return "Server registered."

# Register methods
manager.registerMethod(string)
manager.registerMethod(serverRegister)

# Run manager
manager.run()