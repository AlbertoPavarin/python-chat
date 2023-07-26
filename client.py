import socket
import sys
import signal
import threading
from functools import partial

# COSTANTS
ADDRESS = socket.gethostbyname(socket.gethostname()) # SERVER address, pc address bc server and client are in the same PC
SERVER_PORT = 2222 # port number to connect to server
SOCK = (ADDRESS, SERVER_PORT) # tuple used for connection (x.y.z.k, ####)
FORMAT = 'utf-8' # format with which message are encoded and decoded
DISC_MSG = "!DISC!"
CONNECTED = True
run = True

def signal_handler(client, signal, frame):
    global run
    """
    handler for SIGINT, close the connection to the server and quit the program

    :param :client client socket
    :param :signal type of signal
    :param :frame stack frame, memory zone, which containes datas needed by the executing subroutine
    """
    client.send(DISC_MSG.encode(FORMAT))
    client.close()
    run = False
    print("\nPress Enter to exit")

def set_username():
    username = input("Choose a username: ")
    return username
        

def receive(client): # function to receive messages
    global run
    while run:
        try:
            msg = client.recv(1024).decode(FORMAT)
            print(f'{msg}')
            if msg == DISC_MSG:
                client.close()
                print("\nServer closed\nPress Enter to exit")
                break
        except:
            break

def write(client): # function to send messages
    global run
    while run:
        try:
            msg = input()
            client.send(msg.encode(FORMAT))
            if msg == DISC_MSG:
                client.close()
        except:
            break

def main():
    username = set_username()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creation of the socket
    
    try:
        client.connect(SOCK) # connection to server
    except ConnectionRefusedError:
        sys.exit("Connection Error")

    signal.signal(signal.SIGINT, partial(signal_handler, client))

    client.sendall(username.encode(FORMAT))

    print(f'{ADDRESS}: {client.recv(1024).decode(FORMAT)}')

    threading.Thread(target=receive, args=(client,)).start()
    threading.Thread(target=write, args=(client,)).start()

if __name__ == "__main__":
    main()