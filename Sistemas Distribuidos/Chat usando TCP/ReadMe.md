# Chat TCP 
- Linguagem utilizada: Python
- Comunicação TCP entre cliente e servidor
- Suporte a comandos
- Bibliotecas utilizadas:
    - Socket
    - Threading
  
## Escopo
Consiste em implementar um Chat usando TCP. O Chat deve suportar múltiplos clientes e um servidor. Todos os clientes devem estar na mesma sala do chat (as mensagens enviadas por um cliente devem ser recebidas por todos os clientes). Comandos que o usuário (cliente) pode enviar:
- /ENTRAR: ao usar esse comando, ele é requisitado a digitar IP, porta do servidor e nickname que deseja usar no chat (não precisa tratar nicknames repetidos);
- Uma vez conectado, o cliente pode enviar mensagens para a sala do chat;
- /USUARIOS: ao enviar esse comando, o cliente recebe a lista de usuários atualmente conectados ao chat;
- /SAIR: ao enviar esse comando, uma mensagem é enviada à sala do chat informando que o usuário está saindo e encerra a participação no chat.
- É papel do servidor receber as requisições dos clientes e encaminhar as mensagens recebidas para todos eles. Não pode usar comunicação em grupo.

## Client.py
Ao executar, o usuário deve digitar '/ENTRAR' para realizar a conexão via TCP com server.py. O usuário deve digitar IP e Porta do servidor, além do seu nickname no chat. Após realizar a conexão, abrimos uma thread de write() e receive() para esse cliente. Dessa forma, ele poderá escrever ou receber mensagens de forma independente e paralela em relação ao servidor. O uso de threads também permite a conexão e uso do Chat por outros clientes. Uma vez conectado o usuário pode escrever mensagens (estas serão enviadas a todos os outros usuários), além de realizar dois comandos: /USUARIOS (que retorna exclusivamente a esse usuário a lista de usuários conectados ao servidor naquele momento) e /SAIR (que desliga a conexão deste cliente com o servidor).

## Server.py
O servidor é ligado e abre conexão TCP. Utilizamos o AF_INET pela relação com o ipv4 e o SOCKET_STREAM que está relacionado com a conexão TCP. A função bind() fixa o endereço ADDR do servidor para facilitar a conexão dos clientes a ele. A função receive() realiza a conexão com o cliente, armazenando esse cliente no array clients e o seu nickname respectivo no array nicknames. Após essa conexão, o server.py abre uma thread de hangle() ao cliente. Essa função handle() é responsável por receber mensagem do cliente, processá-la e enviar uma resposta / ação a partir dessa mensagem recebida. Tendo uma thread dessa função, o servidor irá realizar essa operação para cada cliente independente dos demais, permitindo uma execução em paralelo.

A função broadcast() é responsável por realizar o envio de uma mensagem para todos os usuários. Caso algum usuário envie uma mensagem, seja conectado ao servidor ou se desconecte do servidor todos os demais são notificados via essa função de broadcast(). 

A função commands() é responsável por processar um comando que o usuário digite. Caso o usuário digita /USUARIOS, ocorre o envio do array nicknames para todos os demais clientes, com auxilio da função all_users().

A função disconnect() é responsável pelo processo de desconexão do cliente do servidor. Além da remoção deste dos arrays nicknames e clients, ocorre a notificação da saída aos outros usuários, além do fechamento da conexão com o cliente. Tanto no server.py como no client.py existe um break dentro das funções que são usadas nas Threads justamente para concluir sua execução junto com o término da conexão. 
