import socket
from calculator import calculate

server_name = 'Localhost'
server = socket.gethostbyname(socket.gethostname())
server_port = 12456
ADDR = (server, server_port)
FORMAT = 'utf-8'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(ADDR)

print('The server is connected')
print('Target IP: ', server_name)
print('Target Port:', server_port)
print('\n')

while 1:
    number1, number2, operator = 0, 0, 0

    number1, clientAddress = server_socket.recvfrom(2048)
    number1_decoded = float(number1.decode(FORMAT))
    print('Number1 received: ', number1_decoded)

    number2, clientAddress = server_socket.recvfrom(2048)
    number2_decoded = float(number2.decode(FORMAT))
    print('Number2 received: ', number2_decoded)

    operator, clientAddress = server_socket.recvfrom(2048)
    operator_decoded = operator.decode(FORMAT)
    print('Operator received: ', operator_decoded)

    print('Calculating...')
    result = calculate(number1_decoded, number2_decoded, operator_decoded)
    if result != None:
        answer = str(result).encode(FORMAT) 
    else:
        msg = "Invalid Operation"
        answer = msg.encode(FORMAT) 
        
    server_socket.sendto(answer, clientAddress)

    again, clientAddress = server_socket.recvfrom(2048)
    again_decoded = int(again.decode(FORMAT))
    print('Again?', again_decoded)

    if again_decoded == 0:
        break

server_socket.close()