import socket
import sys
import signal
from functools import partial

# COSTANTS
ADDRESS = socket.gethostbyname(socket.gethostname()) # SERVER address, pc address bc server and client are in the same PC
SERVER_PORT = 2222 # port number to connect to server
SOCK = (ADDRESS, SERVER_PORT) # tuple used for connection (x.y.z.k, ####)
FORMAT = 'utf-8' # format with which message are encoded and decoded
DISC_MSG = "!DISC!"
CONNECTED = True

def signal_handler(client, signal, frame):
    """
    handler for SIGINT, close the connection to the server and quit the program

    :param :client client socket
    :param :signal type of signal
    :param :frame stack frame, memory zone, which containes datas needed by the executing subroutine
    """
    client.send(DISC_MSG.encode(FORMAT))
    client.close()
    sys.exit("Disconnected")

def main():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creation of the socket
    client.connect(SOCK) # connection to server

    signal.signal(signal.SIGINT, partial(signal_handler, client))

    print(f'{ADDRESS}: {client.recv(1024).decode(FORMAT)}')

    while CONNECTED:
        msg = input("Type: ")
        if msg == DISC_MSG:
            client.send(msg.encode(FORMAT))
            client.close()
            sys.exit("Disconnected")

        client.send(msg.encode(FORMAT))
        print(f'{ADDRESS}: {client.recv(1024).decode(FORMAT)}')


if __name__ == "__main__":
    main()