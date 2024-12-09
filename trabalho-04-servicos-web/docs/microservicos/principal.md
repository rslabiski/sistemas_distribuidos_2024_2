Microsserviço `Principal`

- em API REST ou gRPC
- Recebe requisições REST do frontend para:
  - visualizar produtos
  - inserir produtos do carrinho
  - atualizar produtos do carrinho
  - remover produtos do carrinho
  - realizar pedidos
  - excluir pedidos
  - consultar pedidos.
- Cada novo pedido recebido será publicado (publisher) como um evento no tópico `Pedidos_Criados`, cujas mensagens serão consumidas pelos microsserviços `Estoque` e `Pagamento`.
- Para atualizar status de cada pedido, consumirá eventos (subscriber) dos tópicos:
  - `Pagamentos_Aprovados`
  - `Pagamentos_Recusados`
  - `Pedidos_Enviados`
- `!` O principal usa o rest_get para o Estoque para visualizar os produtos disponíveis
- Quando um cliente excluir um pedido, o Principal publicará no tópico `Pedidos_Excluídos`.
- Quando o pagamento de um pedido for recusado, o Principal publicará no tópico `Pedidos_Excluídos`.