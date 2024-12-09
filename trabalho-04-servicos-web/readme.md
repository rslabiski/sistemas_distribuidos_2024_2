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

## Microsserviços
- [Estoque](./docs/microservicos/entrega.md)
- [Principal](./docs/microservicos/principal.md)
- [Pagamento](./docs/microservicos/pagamento.md)
- [Entrega](./docs/microservicos/entrega.md)
- [Notificação](./docs/microservicos/notificação.md)

Tópicos
- [Topicos](./topicos.md)

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