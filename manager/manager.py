# Essential Libraries
import socket
import threading

# Thread body
def thread(conn, addr, servers):
    while True:
        print()
        print(servers)
        # Receive data
        data = conn.recv(1024).decode("utf-8")

        # Loop breaker
        if not data:
            print(f"\n> Manager status: No data received from {addr[0]}:{addr[1]}.")
            print(f"> Manager status: Closing connection...")
            break

        # Show data
        print(f"\n> Data from {addr[0]}:{addr[1]}: {data}")

        # Return data
        print(f"> Manager Status: Returning data...")
        conn.sendall(data.encode("utf-8"))
        print("> Manager Status: Data sent successfully!")

    # Close connection
    conn.close()
    print(f"> Manager status: Connection closed.")
    servers.remove(addr)


def Main():
    # Manager info
    HOST = "127.0.0.1"  # network interface (IPv4)
    PORT = 65432        # port number

    # All threads array
    threads = []

    # All servers address
    servers = []

    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Associate the socket with the manager info
        s.bind((HOST, PORT))

        # Ennable the manager accept connections
        s.listen()
        print("> Manager Status: ON.")

        try:
            while True:
                # Accept a connection
                conn, addr = s.accept()
                print(f"\n> Manager Status: Connected with {addr[0]}:{addr[1]}")
                servers.append(addr)

                # Create and start a thread
                t = threading.Thread(target=thread, args=(conn, addr, servers))
                t.start()

                # Append thread
                threads.append(t)
        except:
            print("\nManager closed unexpectedly.")
        finally:
            if s:
                s.close()   # Close socket
            for t in threads:
                t.join()    # Wait thread finish

if __name__ == '__main__':
    Main()