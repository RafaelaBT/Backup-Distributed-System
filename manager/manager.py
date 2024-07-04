import socket

# Manager info
HOST = "127.0.0.1"  # network interface (IPv4)
PORT = 65431        # port number

# Creates the s socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Associates the socket with the manager info
    s.bind((HOST, PORT))

    # Ennable the manager accept connections
    s.listen()
    print("> Manager Status: ON.")
    print("> Manager Status: Waiting for connection...")

    # Accept a connection
    conn, addr = s.accept()
    print("> Manager Status: Connection accepted.")

    # Connection established
    with conn:
        print(f"> Manager Status: Connected with {addr}")

        # While there is a connection
        while True:

            # Receive data
            print(f"> Manager Status: Receiving data...")
            data = conn.recv(1024).decode("utf-8")

            # Loop breaker
            if not data:
                print(f"> Manager status: No data received.")
                print(f"> Manager status: Exiting Manager...")
                break

            print(f"> Data: {data}")

            # Send data
            print(f"> Manager Status: Returning data...")
            conn.sendall(data.encode("utf-8"))
            print("> Manager Status: Data sent successfully!")