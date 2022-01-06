import socket
import threading

server_name = 'Localhost'
server = socket.gethostbyname(socket.gethostname())
server_port = 12456
ADDR = (server, server_port)
FORMAT = 'utf-8'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)
server_socket.listen()

print("Server On!")
print("IP's Server: ", ADDR)

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def commands(client, message):
    if message == '/USUARIOS':
        all_users(client)   
    else:
        client.send("Invalid message! Please try again...".encode(FORMAT))

def all_users(client):
    client.send('{}'.format(nicknames).encode(FORMAT))

def disconnect(client):
    client.send('Disconnecting...'.encode(FORMAT))
    index = clients.index(client)
    clients.remove(client)
    client.send('Disconnected!'.encode(FORMAT))
    client.close()
    nickname = nicknames[index]
    print('{} left!'.format(nickname))
    broadcast('{} left!'.format(nickname).encode(FORMAT))
    nicknames.remove(nickname)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            message_decoded = message.decode(FORMAT)
            if message_decoded[0] == '/':
                if message_decoded == '/SAIR':
                    disconnect(client)
                    break
                commands(client, message_decoded)
            else:
                broadcast(message)
        except:
            disconnect(client)
            break

def receive():
    while True:
        client, address = server_socket.accept()
        print("Connected with {}".format(str(address)))

        client.send('NICK'.encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        nicknames.append(nickname)
        clients.append(client)

        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode(FORMAT))
        client.send('Connected to server!'.encode(FORMAT))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
