# Notas do enunciado

## Front end
Os clientes irão interagir com a aplicação para:
- visualizar produtos
- inserir produtos do carrinho
- atualizar produtos do carrinho
- remover produtos do carrinho
- realizar pedidos
- excluir pedidos
- consultar pedidos.

O Frontend é uma aplicação web que deve ser implementada em uma linguagem diferente do backend.

Frontend
- `!` Será em Java Script
- Essa aplicação consumirá a API REST ou gRPC
- Receberá notificações via SSE (Server Sent Events).

O SSE é uma tecnologia que permite que um servidor envie atualizações em tempo real para clientes via HTTP, utilizando um único canal de comunicação unidirecional. Diferente do WebSocket, que estabelece uma comunicação bidirecional, o SSE é projetado especificamente para enviar dados do servidor para os clientes, tornando-o ideal para aplicações que necessitam de notificações em tempo real ou atualizações contínuas.

## Back end
`!` O Backend será em Python

O backend
- Possui cinco microsserviços independentes
- Os microsserviços devem se comunicar com outros microsserviços de maneira assíncrona e desacoplada através de um sistema de mensageria (RabbitMQ)

Microsserviço Principal
- em API REST ou gRPC
- Recebe requisições REST do frontend para:
  - visualizar produtos
  - inserir produtos do carrinho
  - atualizar produtos do carrinho
  - remover produtos do carrinho
  - realizar pedidos
  - excluir pedidos
  - consultar pedidos.
- Cada novo pedido recebido será publicado (publisher) como um evento no tópico `Pedidos_Criados`, cujas mensagens serão consumidas pelos microsserviços Estoque e Pagamento.
- Consumirá eventos (subscriber) dos tópicos `Pagamentos_Aprovados`, `Pagamentos_Recusados` e `Pedidos_Enviados` para atualizar o status de cada Pedido.
- `!` O principal usa o rest_get para o Estoque para visualizar os produtos disponíveis
- Quando um cliente excluir um pedido, o Principal publicará no tópico `Pedidos_Excluídos`.
- Quando o pagamento de um pedido for recusado, o Principal publicará no tópico `Pedidos_Excluídos`.


Microsserviço `Estoque`
- Gerencia o estoque de produtos.
- Ele consumirá eventos do tópico `Pedidos_Criados` e `Pedidos_Excluídos`.
- Quando um pedido for criado, atualizar o estoque.
- Quando um pedido for excluído, atualizar o estoque.
- Quando um pagamento for recusado, atualizar o estoque.
- Responde requisições REST ou gRPC do microsserviço Principal, enviando dados dos produtos em estoque.

Microsserviço Pagamento:
- Gerencia os pagamentos através da integração com um sistema externo de pagamento via Webhook.
- É necessário definir uma URL (isto é, um endpoint) que irá receber:
  - notificações de pagamento aprovado
  - notificações de pagamento recusado.
- Se o pagamento for aprovado, publicará o evento no tópico `Pagamentos_Aprovados`.
- Se o pagamento for recusado, publicará o evento no tópico `Pagamentos_Recusados`, para que o sistema cancele o pedido e atualize o estoque.

Microsserviço Entrega:
- Gerencia:
  - emissão de notas
  - entrega dos produtos
- Consome eventos do tópico `Pagamentos_Aprovados`
- Publica no tópico `Pedidos_Enviados`.

Microsserviço Notificação:
- Notifica via SSE para o frontend sempre que houver alteração no status de pedidos
  - pedido criado
  - pagamento aprovado
  - pagamento recusado
  - pedido enviado.
- Essas notificações devem incluir o ID e o status do pedido.
- Este serviço consome eventos de todos os tópicos.

Tópico Pedidos_Criados
- Mensagens serão consumidas pelos microsserviços Estoque e Pagamento.
- Subscribers:
  - Estoque
  - Pagamento
  - Notificação
- Publishers:
  - Principal

Tópico Pagamentos_Aprovados
- Subscribers:
  - Principal
  - Notificação
  - Entrega
- Publishers:
  - Pagamento

Tópico Pagamentos_Recusados
- Subscribers:
  - Principal
  - Notificação
- Publishers:
  - Pagamento

Tópico Pedidos_Enviados
- Subscribers:
  - Principal
  - Notificação
- Publishers:
  - Entrega

Tópico Pedidos_Excluídos
- Subscribers:
  - Notificação
  - Estoque
- Publishers:
  - Principal

## Sistema de Pagamento

Sistema de pagamento
- deve ser responsável por processar os pagamentos.
- Nesse sistema será configurado um Webhook.
- Após a autorização ou recusa de cada pagamento, o sistema de pagamento enviará uma notificação assíncrona (HTTP POST) via webhook para o endpoint configurado no backend do e-commerce.
- O corpo da requisição POST conterá detalhes sobre o evento:
  - ID da transação
  - status do pagamento (autorizado, recusado, estornado, etc.)
  - valor
  - dados do comprador.

Webhooks são mais comumente usados para comunicação entre servidores de forma assíncrona, enquanto o REST é um padrão de comunicação cliente-servidor que geralmente envolve interações (operações CRUD) síncronas iniciadas e controladas pelo cliente.

Webhooks são ideais para notificar um servidor sobre a ocorrência de um evento em outro servidor. Ele é especialmente útil quando uma aplicação não precisa de uma resposta imediata. Por exemplo, serviços de pagamento usam Webhooks para notificar sistemas sobre o status de pagamentos. Quando um pagamento é processado com sucesso, o serviço de pagamento notifica automaticamente (callback) o sistema de destino via uma requisição HTTP POST, informando o status da transação. O sistema de destino, então, pode atualizar o status do pedido com base nos eventos externos recebidos. Isso torna a comunicação mais eficiente e escalável, sem a necessidade de manter conexões abertas ou fazer chamadas repetitivas (polling) para saber se um evento ocorreu.

- `!` O cliente interage com o sistema de pagamento para que o pedido possa ser aprovado/recusado.

Observações:
- Desenvolva uma interface com recursos de interação apropriados.
- É obrigatória a defesa da aplicação para obter a nota.
- O desenvolvimento do sistema pode ser individual ou em dupla