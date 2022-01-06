import socket
import threading

FORMAT = 'utf-8'
connected = 0

def receive(client_socket, nickname):
    global connected
    while True:
        try:
            message = client_socket.recv(1024).decode(FORMAT)
            if message == 'NICK':
                client_socket.send(nickname.encode(FORMAT))
            elif message == 'Disconnected!!':
                print(message)
                connected = 0
                client_socket.close()
                break
            else:
                print(message)
        except Exception as e:
            print(e)

def write(client_socket, nickname):
    global connected
    while True:
        try:
            if connected == 1:
                text = input('')
                if text[0] == '/':
                    client_socket.send(text.encode(FORMAT))
                else:
                    message = '{}: {}'.format(nickname, text)
                    client_socket.send(message.encode(FORMAT))
        except Exception as e:
            print(e)

if connected == 0:
    input_i = input('')
    if input_i == '/ENTRAR':
        print("To make the connection, we ask for the IP, server port and nickname.")
        server = input("IP's Server: ")
        port = input("Port's Server: ")
        nickname = input("Choose your nickname: ")

        ADDR = (server, int(port))

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(ADDR)
            print("Server Conected!")

            connected = 1
            receive_thread = threading.Thread(target=receive, args=(client_socket, nickname))
            receive_thread.start()

            write_thread = threading.Thread(target=write, args=(client_socket, nickname))
            write_thread.start()

        except Exception as e:
            print(e)