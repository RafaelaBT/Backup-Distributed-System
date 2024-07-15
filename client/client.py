# Import modules
import sys, os
path = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.append(path + '../')
from RPC.RPCClient import RPCClient

# Create client
client = RPCClient()

# Connect client to server
client.connect()

print("\n( • ֊ •)づ Hello, welcome to BACKUP SYSTEM!")
while True:
    if client.isConnected():
        print("\n──────────────── ⋆ ☆ MENU ☆ ⋆ ─────────────────")
        print("\n1 - UPLOAD")
        io = input("\nWrite the option number or press ENTER to exit: ")

        if io == "":
            print("\n(„• ֊ •„)੭ Byee, see you later!")
            break

        # Call procedures
        if io == "1":

            filename = "plano-ensino-sd-q2-2023.pdf"
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
