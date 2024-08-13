# Import modules
from RPCManager import RPCManager

# Create server
manager = RPCManager()

# Return string
def string(s:str):
    return s

# Add server
def addServer(addr:tuple, capacity:int):
    return manager.serverRegister(addr, capacity)

# Remove server
def removeServer(addr:tuple):
    return manager.delServer(addr)

# Choose server
def getServer(addr:tuple=None):
    return manager.chooseServer(addr)

# Update server capacity
def updateServer(addr:tuple, capacity:int):
    return manager.updateCapacity(addr, capacity)

# Return connected servers number
def getQuantity():
    return manager.getSize()

# Register methods
manager.registerMethod(string)
manager.registerMethod(addServer)
manager.registerMethod(removeServer)
manager.registerMethod(getServer)
manager.registerMethod(updateServer)
manager.registerMethod(getQuantity)

# Run manager
manager.run()
