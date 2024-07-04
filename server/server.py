import socket

# Manager info
HOST = "127.0.0.1"
PORT = 65432

# Creates the s socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Try to connect with Manager
    print("> Server Status: Trying to connect with Manager...")
    s.connect((HOST, PORT))
    print("> Server Status: Connection accepted.")

    while True:
        
        # Input text data
        msg = input("> Write a message: ")

        if msg == "":
            print("> Server Status: No data sent.")
            print("> Server Status: Exiting server...")
            break

        # Sends data to Manager
        print("> Server Status: Sending data...")
        s.sendall(msg.encode("utf-8"))
        print("> Server Status: Data sent successfully!")

        # Receives data from Manager
        print("> Server Status: Receiving data...")
        data = s.recv(1024).decode("utf-8")
        print(f"> Data: {data}")