# Import modules
from RPCManager import RPCManager

# Create server
manager = RPCManager()

# Return string
def string(s:str):
    return s

def addServer(addr:tuple, capacity:int):
    return manager.serverRegister(addr, capacity)

def removeServer(addr:tuple):
    return manager.delServer(addr)

def getServer():
    return manager.chooseServer()

def updateServer(addr:tuple, capacity:int):
    return manager.updateCapacity(addr, capacity)

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