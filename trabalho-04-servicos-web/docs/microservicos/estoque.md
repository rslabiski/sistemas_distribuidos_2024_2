Microsserviço `Estoque`

- Gerencia:
  - estoque de produtos.
- Ele consumirá eventos do tópico `Pedidos_Criados`.
- Ele consumirá eventos do tópico `Pedidos_Excluídos`.
- Quando um pedido for criado, atualizar o estoque.
- Quando um pedido for excluído, atualizar o estoque.
- Quando um pagamento for recusado, atualizar o estoque.
- Responde requisições REST ou gRPC do microsserviço `Principal`, enviando dados dos produtos em estoque.