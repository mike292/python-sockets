import socket

PORT = 5050
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECTED!"
SERVER = "192.168.1.11"  # this depends on what server the client is connecting to
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    # the send_length is just 2 bytes, it must be 64
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    # receive message from the server
    print(client.recv(2048).decode(FORMAT))


send("Hello World!")
input()
send("Hello Everyone!")
input()
send("Hello Mike!")
input()
send(DISCONNECT_MESSAGE)
