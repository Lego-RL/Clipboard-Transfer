import pyperclip
import socket
import sys


DISCONNECT_MSG = '!DISCONNECT'
HEADER = 16
FORMAT = 'utf-8'

PORT = 5050
SERVER = '10.0.0.160'
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Connecting...')
client.connect(ADDR)

def send(msg):
    try:
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)

        padded_length = send_length + ((HEADER - len(send_length)) * b' ')
        client.send(padded_length)
        client.send(message)
        print(client.recv(64).decode(FORMAT))
    
    except ConnectionResetError:
        print('Server connection ended')
        sys.exit(0)



while True:
    inp = input('ENTER to send clipboard to laptop, -1 to exit. ')
    if inp == '-1':
        sys.exit(0)
    
    else:
        send(pyperclip.paste())