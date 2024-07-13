# Import modules
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from RPC.RPCServer import RPCServer

# Create server
server = RPCServer()

# Return string
def string(s):
    return s

# Add two numbers
def add(a, b):
    return a+b

# Sub two numbers
def sub(a, b):
    return a-b

# Register methods
server.registerMethod(string)
server.registerMethod(add)
server.registerMethod(sub)

# Run server
server.run()