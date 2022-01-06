# Projeto de Calculadora
- Linguagem utilizada: Python
- Comunicação UDP entre cliente e servidor
- Bibliotecas utilizadas:
  - Socket

## Escopo
Calculadora_UDP: consiste em, utilizando UDP, implementar uma calculadora remota que execute as 4 operações básicas (+, -, x, /) de números decimais. Descreva o formato para cada tipo das mensagens (Request e Response).

## Client.py
O Client.py realiza a conexão UDP com o server.py. (Iniciamos inicialmente o server.py para ligar o servidor e abrir a conexão via UDP). Na linha 10, AF_INET está relacionado com o ipv4 e o SOCK_DGRAM é utilizado propriamente para conexão UDP. 
Input dos números e dos operadores. Se os inputs forem do tipo numéricos realiza-se o envio dos números e do operador ao server.py. Ao mesmo tempo, que aguarda o recebimento da mensagem do server.py com a resposta do cálculo.

## Server.py
O server é ligado estabelecendo conexão UDP de forma semelhante que ocorreu ao Client.py. A diferença é que utilizamos a função bind() para fixar o ADDR do servidor. Após conexão ao client.py via UDP, o server.py aguarda recebimento dos números e operador. Chama a função calculate() de Calculator.py que recebe os dois números e baseado no operador realiza a operação e retorna seu resultado. Após isso o server.py realizar o envio desse resultado ao Client.py.
