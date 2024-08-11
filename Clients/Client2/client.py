# Import modules
import sys, os
path = os.path.dirname(os.path.abspath(__file__)) + '/Files/'
sys.path.append(path + '../../')
from RPCClient import RPCClient

print("\n( • ֊ •)づ Hello, welcome to BACKUP SYSTEM!")

# Create client
client = RPCClient()

# Connect client to manager
client.connect()

while True:
    if client.isConnected():
        print("\n──────────────── ⋆ ☆ MENU ☆ ⋆ ─────────────────")
        # List files
        files = os.listdir(path)
        for file in files:
            print(file)

        # Get filename from user
        filename = input("\nWrite the file name or press ENTER to exit: ")

        # Exit system
        if filename == "":
            print("\n(„• ֊ •„)੭ Byee, see you later!")
            break

        # Check filename
        if filename in files:
            # Send file
            if client.sendFile(path, filename):
                print("\n( •̀  ᴗ ´•̀)✧ File sent successfully!")
            else:
                print("\n【• _ • ?】An error occurred, please try again later.")
        else:
            print("\n( ô ‸ ō )....????? Sorry, I don't know this option.")
            print("\n(  •̀ ᴗ - )ᕤ But don't worry, lets try again!")
    else:
        print("\n( ╥ ᴗ ╥) Sorry, server is not available. Please try again later.")
        break

# Diconnect client
client.disconnect()
