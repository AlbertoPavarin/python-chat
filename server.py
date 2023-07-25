import socket
import threading
import signal
import sys
from functools import partial

# COSTANTS
ADDRESS = socket.gethostbyname(socket.gethostname()) # SERVER address, pc address bc server and client are in the same PC
SERVER_PORT = 2222 # port number to connect to server
SOCK = (ADDRESS, SERVER_PORT) # tuple used for connection (x.y.z.k, ####)
FORMAT = 'utf-8' # format with which message are encoded and decoded
DISC_MSG = "!DISC!"
CONNECTED = True

def client_connection(comm_sock, remote_addr):
    print(f"Conected with {remote_addr}")
    comm_sock.send("Connected with server".encode(FORMAT))
    while True:
        msg = comm_sock.recv(1024).decode(FORMAT)
        print(f'{remote_addr}: {msg}')
        if msg == DISC_MSG:
            comm_sock.close()
            break
        comm_sock.send("Message received".encode(FORMAT))

def signal_handler(server, signal, frame):
    """
    handler for SIGINT, closes the server socket and quits the program

    :param :server server socket
    :param :signal type of signal
    :param :frame stack frame, memory zone, which containes datas needed by the executing subroutine
    """
    # should close every connection, then exit, to implement
    server.close()
    sys.exit("Server closed")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket creation
    server.bind(SOCK)

    signal.signal(signal.SIGINT, partial(signal_handler, server))

    server.listen()
    while CONNECTED:
        comm_sock, remote_addr = server.accept() # accept a comunication
        threading.Thread(target=client_connection, args=(comm_sock, remote_addr)).start()
        """creates and starts a ne thread to handle a connection, 
           providing multiple connection at the same time"""

    server.close()
    

if __name__ == "__main__":
    main()