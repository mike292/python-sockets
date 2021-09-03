import socket
import threading

DISCONNECT_MESSAGE = "DISCONNECTED!"
FORMAT = "utf-8"
HEADER = 64  # amount bytes we can receive from a client at a time
# which port where the server will run on
PORT = 5050
# SERVER = "192.168.1.11" # goto cmd and type 'ipconfig, to run on local'


# or use socket to get the local up address
# gethostbyname method gets the ip of the local by the name of the computer
# gethostname method gets the this device name
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)  # the address must be tuple

# creates a socket - where clients can connect to
# AF_INET - what kind of address that will be connecting
# SOCK_STREAM - streaming data into the socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binds this socket to the ip and port(address)
server.bind(ADDR)


def handle_client(conn, addr):  # handles individual connections (1 client per execution)
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
        # conn.recv() is a blocking code - wait until it has received a msg from the client
        # it will return a byte type must be decoded with utf-8 format
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:  # when it first connected it will send a null, this blocks that
            msg_length = int(msg_length)
            # the first recv will get the size of the message before the actual message
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")

            # send message back to the client
            conn.send("Message received.".encode(FORMAT))
    conn.close()


def start():  # start the socket server, handles new connections
    # starts listening for connections
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}")
    while True:
        # conn - an object we use to communicate to the connected client
        # addr - the address of the connected client
        # blocking code - while the server is listening this code will wait for a connection
        conn, addr = server.accept()

        # creates a new thread for a new connected client and passes it to the handle_client function
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        # how many active threads(clients)
        # - 1 because the server is considered an active thread
        print(f"[ACTIVE CONNECTION] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
