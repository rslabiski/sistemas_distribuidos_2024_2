Microsserviço `Notificação`

- Notifica via SSE para o frontend sempre que houver alteração no status de pedidos
  - pedido criado
  - pagamento aprovado
  - pagamento recusado
  - pedido enviado.
- Essas notificações devem incluir o ID e o status do pedido.
- Este serviço consome eventos de todos os tópicos.