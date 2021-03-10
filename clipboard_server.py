import pyperclip
import socket
import threading


DISCONNECT_MSG = '!DISCONNECT'
HEADER = 16
FORMAT = 'utf-8'

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f'[NEW CONNECTION]{addr} connected')

    while True:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)

            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)

                if msg == DISCONNECT_MSG:
                    break
                
                else:
                    print(f'[RECEIVED] Pasting {msg}')
                    copy_to_clipboard(msg)
                    conn.send('[SERVER RESPONSE] Data received'.encode(FORMAT))

        except ConnectionResetError: #client connection ended
            conn.close()
            print(f'[DISCONNECTED] {addr}')
            return

    conn.close()
    print(f'[DISCONNECTED] {addr}')


def copy_to_clipboard(msg):
    pyperclip.copy(msg)


def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f'[CONNECTIONS]: {threading.activeCount() - 1}')

print("[STARTING] Server is starting")
start()