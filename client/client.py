# Import modules
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from RPC.RPCClient import RPCClient

# Create client
client = RPCClient()

# Connect client to server
client.connect()

if client.isConnected():
    # Call procedures
    print(client.add(5, 6))
    print(client.sub(5, 6))

    # Diconnect client
    client.disconnect()