# Ambiente Inteligente
- Linguagem utilizada: Python
- Uso de multicast para identificação de novos objetos
- Comunicação TCP entre objetos e gateway
- Comunicação TCP como uso de protocol buffers entre aplicação e gateway
- Suporte a comandos
- Bibliotecas utilizadas:
  - Socket;
  - Threading;
  - Time;
  - Struct;
  - Protocol Buffers.

## Escopo
- Uma aplicação (móvel, desktop ou web) deve ser implementada para permitir ao usuário conectar e visualizar o status dos objetos do ambiente inteligente, além de atuar e ler os dados dados dos objetos.
- A aplicação deve se conectar a um servidor, chamado de Gateway, que se comunica com cada um dos objetos "inteligentes" do local. A comunicação entre aplicação e o Gateway deve ser implementada utilizando TCP e as mensagens definidas com Protocol Buffers.
- Deve haver, pelo menos, dois tipos de mensagens (Request e Response) cujos formatos devem ser definidos pelo grupo.
- O ambiente inteligente deve conter, no mínimo, 3 equipamentos (lâmpadas, tv, ar condicionado, etc...).
- A comunicação do Gateway com os equipamentos fica a critério do time. Tais equipamentos podem ser todos simulados por software, que envia de forma periodica seu estatus (ou quando ele se modifica) e recebe comandos para ligar/desligar ou realizar alguma operação.
- O Gateway deve ter uma funcionalidade de descobertas de equipamentos inteligentes, usando comunicação em grupo. Ao iniciar o Gateway, ele deve enviar uma mensagem solicitando que os equipamentos se identifiquem.
- Ao iniciar o processo dos equipamentos inteligentes, estes devem enviar mensagem se identificando para o Gateway. A identificação significa enviar seu tipo (lâmpada, ar condicionado, etc..), Ip e Porta para o Gateway.
- Pelo menos um dos equipamentos deve atuar como um sensor contínuo, que envia a cada ciclo de X segundos um valor para o Gateway (um sensor de temperatura).
- Pelo menos um dos equipamentos deve ter comportamento de um atuador (recebe comandos para atualizar seu status, como ligar/desligar).

A intenção do projeto é ter uma aplicação (que simulamos no terminal), esta se conecta ao gateway. Essa conexão ocorre via TCP usando Protocol Buffers. 
Já o Gateway realiza a descoberta de objetos inteligentes via multicast. Ocorre, posteriormente, a conexão do Gateway com esses objetos.
A aplicação pode solicitar status desses objetos e solicitar modificação desses status. Além disso, um dos objetos do projeto deve enviar periodicamente uma atualização ao Gateway do seu status e algum atributo.
Resumindo, é uma simulação de projeto envolvendo IoT. 

Devido a complexidade desse projeto, iremos apenas dar uma visão geral do projeto. Recomenda-se visualizar o projeto Chat_TCP antes de visualizar esse projeto.

## Objetos Usados
- Lâmpada (LAMP.PY)
  - Status: ligado / desligado
  - ENVIO DO STATUS QUANDO SOLICITADO
- BORRIFADOR (SPRINKLER.PY)
  - STATUS: LIGADO / DESLIGADO
  - ENVIO DO STATUS QUANDO SOLICITADO
- AR CONDICIONADO (AC.PY)
  - STATUS: LIGADO / DESLIGADO
  - TEMPERATURA
  - ENVIO periodico DE SUA TEMPERATURA E STATUS

Essas funções que representam os objetos se encontram dentro da pasta objects.

## Lógica Multicast
Funcionalidade de descoberta de objetos inteligentes, usando comunicação em grupo (multicast).

- GATEWAY ENVIA O IP E PORTA PARA OS OBJETOS
- OBJETOS RECEBEM ADDR DO GATEWAY PARA REALIZAR CONEXÃO TCP POSTERIORMENTE

### receive_multicast_group.py
Recebimento de mensagem via multicast (função que é herdada pelo client.py).

Em client.py existe a função get_addr_by_mult(), que é responsável pelo recebimento do endereço do gateway (IP, PORT). Os objetos herdam a classe Client.

Logo, todos os objetos recebem uma mensagem contendo o IP e Porta do Gateway.

### send_multicast_group.py
Envio de mensagem via multicast (Função que é herdada pelo gateway.py)

No gateway.py a função send_gateway_address() realiza o envio da mensagem contendo seu IP e Porta. 

Logo, o gateway envia uma mensagem com seu IP e Porta para todos os clientes conectados ao multicast, ou seja, a todos os objetos. Mesmo que estes não estejam diretamente conectados ao gateway.

## Conexão TCP
Realiza após todos os objetos terem sido descobertos pelo gateway, estes terem recebido seu addr. Os objetos enviam o seu tipo, IP e PORTA ao gateway durante a conexão TCP.

### Client.py
A função connect_tcp() que ao inserir o ADDR do Gateway realiza a conexão com o mesmo via TCP. Após a conexão, abre a thread da função receive(), dessa forma o cliente pode receber mensagens do gateway independente dos demais clientes. Consequentemente, essa lógica funciona para os objetos, já que os objetos herdam Client.

### Gateway.py
A função start_server() liga gateway.py para conexões TCPs.
A função connect_client_by_tcp() que realiza a conexão TCP com os objetos e a aplicação.

Resumindo, após cada objeto receber o ADDR do Gateway via multicast (essa funcionalidade fica ativada apenas por alguns segundos), este usam esse ADDR para conectar via TCP com o gateway, informando seu tipo (objeto), IP e Porta do objeto. 

O Gateway abre a thread da função handle_application() para fazer a "conversa" entre aplicação e gateway via TCP e Protocol Buffers. Para coisas diferentes da aplicação, após a conexão, o gatway inicia a thread da função handle() para fazer a "conversa" entre gateway e objetos via TCP, sem necessidade do uso do Protocol Buffers.

### Application.py
Ao ligar a aplicação, esta já realiza a conexão com o gateway via TCP.
Após a conexão, inicia-se a thread receive() em que a aplicação poderá receber mensagens do gateway de forma independente.

Diferente do que foi feito no Chat_TCP, abrimos threads apenas para recebimento de mensagens nos clientes. Pois a função de escrita será executada apenas quando necessário. Ou seja, quando a aplicação solicitar algo.

### main_lamp.py / main_sprinkler.py / main_ac.py
Esses arquivos instanciam os objetos e colocam eles para funcionar. Eles recebem o ADDR via multicast e conectam via TCP com o gateway. Esses arquivos herdam seus objetos, respectivamente. Por exemplo, main_lamp.py herda a classe Lamp em lamp.py. A classe Lamp em lamp.py herda a classe Cliente em client.py, como já foi comentado. Essa lógica de orientação a objetos vale para os outros dois objetos.

## Protocol Buffers
No arquivo de formato .proto contem o formato das mensagens que serão trocadas entre Aplicação e Gateway. ApplicationMessage se refere a mensagens enviadas pela Aplicação ao Gateway. E GatewayMessage se refere a mensagens enviadas pelo Gateway à Aplicação.
