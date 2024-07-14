# Import modules
import sys, os
path = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.append(path + '../')
from RPC.RPCServer import RPCServer

# Create server
server = RPCServer()

# Return string
def string(s):
    return s

def sendData(data):
    filename = data['filename']
    file_content = data['file_content']

    with open(path + filename, 'wb') as file:
        file.write(file_content.encode())

    return f'Recebido arquivo {filename}.'

# Add two numbers
def add(a, b):
    return a+b

# Sub two numbers
def sub(a, b):
    return a-b

# Register methods
server.registerMethod(string)
server.registerMethod(sendData)
server.registerMethod(add)
server.registerMethod(sub)

# Run server
server.run()