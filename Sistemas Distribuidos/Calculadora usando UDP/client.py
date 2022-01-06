from socket import *
import socket

server_name = 'Localhost'
server = socket.gethostbyname(socket.gethostname())
server_port = 12456
ADDR = (server, server_port)
FORMAT = 'utf-8'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect(ADDR)

print("Sucessful Connection!")

while 1:
    number1 = input('Input number1: ')
    number2 = input('Input number2: ')
    operator = input('Input operator (+, -, *, /): ')

    if number1.isnumeric() and  number2.isnumeric():
        client_socket.sendto(number1.encode(FORMAT), ADDR)
        client_socket.sendto(number2.encode(FORMAT), ADDR)
        client_socket.sendto(operator.encode(FORMAT), ADDR)

        answer, clientAddress = client_socket.recvfrom(2048)
        answer_decoded = answer.decode(FORMAT)
        print('Result of Operation: ', answer_decoded)

        again = input('Do you want to do another operation? \n 1 - Yes. \n 0 - No. \n')
        client_socket.sendto(again.encode(FORMAT), ADDR)

        if int(again) == 0:
            break
    else:
        print("Insert a number, please.")

client_socket.close()

