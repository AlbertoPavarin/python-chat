import socket
import threading
import signal
import sys
from functools import partial

def get_ip_address():
    return socket.gethostbyname(socket.gethostname())

# COSTANTS
ADDRESS =  get_ip_address() # SERVER address, pc address bc server and client are in the same PC
SERVER_PORT = 2222 # port number to connect to server
SOCK = (ADDRESS, SERVER_PORT) # tuple used for connection (x.y.z.k, ####)
FORMAT = 'utf-8' # format with which message are encoded and decoded
DISC_MSG = "!DISC!"
CONNECTED = True
connections = []

def client_connection(comm_sock, remote_addr):
    global connections
    username = comm_sock.recv(1024).decode(FORMAT)
    join_alert(username)
    user = {
        'socket': comm_sock,
        'address': remote_addr,
        'username': username
    }
    connections.append(user) 
    print(f"Conected with {user['username']}")
    comm_sock.send("Connected with server".encode(FORMAT))
    comm_sock.send("\nUsers connected:\n".encode(FORMAT))
    for conn in connections:
        comm_sock.send(f" - {conn['username']}\n".encode(FORMAT))
    while True:
        msg = comm_sock.recv(1024).decode(FORMAT)
        print(f'{username}: {msg}')
        send_to_all(user, msg)
        if msg == DISC_MSG:
            connections.remove(user)
            comm_sock.close()
            break
        comm_sock.send("SERVER: Message received".encode(FORMAT))

def signal_handler(server, connections, signal, frame):
    """
    handler for SIGINT, closes the server socket and quits the program

    :param :server server socket
    :param :connections list that containes all the connections to the server
    :param :signal type of signal
    :param :frame stack frame, memory zone, which containes datas needed by the executing subroutine
    """
    # should close every connection, then exit, to implement
    for connection in connections:
        connection['socket'].send(DISC_MSG.encode(FORMAT))
    server.close()
    sys.exit("Server closed")

def send_to_all(sender, msg): # send the messages in broadcasr, to everyone in the chat
    for connection in connections:
        if connection['username'] != sender['username']:
            connection['socket'].sendall(f"{sender['username']}: {msg}".encode(FORMAT))
        
def join_alert(username): # send a message that says a user joined
    for connection in connections:
        if connection['username'] != username:
            connection['socket'].sendall(f"SERVER: {username} joined".encode(FORMAT))

def main():
    global connections
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket creation
    server.bind(SOCK)

    signal.signal(signal.SIGINT, partial(signal_handler, server, connections))

    server.listen()
    while CONNECTED:
        comm_sock, remote_addr = server.accept() # accept a comunication
        threading.Thread(target=client_connection, args=(comm_sock, remote_addr)).start()
        """creates and starts a ne thread to handle a connection, 
           providing multiple connection at the same time"""

    server.close()
    

if __name__ == "__main__":
    main()