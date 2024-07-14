# Import modules
import sys, os
path = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.append(path + '../')
from RPC.RPCClient import RPCClient

# Create client
client = RPCClient()

# Connect client to server
client.connect()

def sendFile(path, filename):
    with open(path + filename, 'rb') as file:
        file_content = file.read().decode()

    data = {
        'filename': filename,
        'file_content': file_content
    }

    client.sendData(data)

    return 

if client.isConnected():
    print("\n( • ֊ •)づ Hello, welcome to BACKUP SYSTEM!")

    while True:
        print("\n──────────────── ⋆ ☆ MENU ☆ ⋆ ─────────────────")
        print("\n1 - ADD\n2 - SUB")
        io = input("\nWrite the option number or press ENTER to exit: ")

        if io == "":
            print("\n(„• ֊ •„)੭ Byee, see you later!")
            break

        # Call procedures
        if io == "1":
            print(sendFile(path, "teste.txt"))

        elif io == "2":
            print(f"SUB = {client.sub(5, 6)}")
        else:
            print("\n( ô ‸ ō )....????? Sorry, I don't know this option.")
            print("\n(  •̀ ᴗ - )ᕤ But don't worry, lets try again!")

    # Diconnect client
    client.disconnect()