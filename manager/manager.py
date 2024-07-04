import socket
import threading

lock = threading.Lock()

def thread(conn, addr):
    # While there is a connection
    while True:

        # Receive data
        print(f"> Manager Status: Receiving data...")
        data = conn.recv(1024).decode("utf-8")

        # Loop breaker
        if not data:
            print(f"> Manager status: No data received.")
            print(f"> Manager status: Closing connection...")
            lock.release()
            break

        print(f"> Data: {data}")

        # Send data
        print(f"> Manager Status: Returning data...")
        conn.sendall(data.encode("utf-8"))
        print("> Manager Status: Data sent successfully!")
    
    conn.close()
    print(f"> Manager status: Connection closed.")


def Main():

    # Manager info
    HOST = "127.0.0.1"  # network interface (IPv4)
    PORT = 65432        # port number

    threads = []

    # Creates the s socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Associates the socket with the manager info
        s.bind((HOST, PORT))

        # Ennable the manager accept connections
        s.listen()
        print("> Manager Status: ON.")
        print("> Manager Status: Waiting for connection...")

        # 
        try:
            while True:

                # Accept a connection
                conn, addr = s.accept()
                print("> Manager Status: Connection accepted.")

                lock.acquire()

                # Connection established
                print(f"> Manager Status: Connected with {addr[0]}:{addr[1]}")

                t = threading.Thread(target=thread, args=(conn, addr))
                t.start()

                threads.append(t)
                    
        except KeyboardInterrupt:
            print("Stopped by Ctrl+C.")
        finally:
            if s:
                s.close()
            for t in threads:
                t.join()

if __name__ == '__main__':
    Main()