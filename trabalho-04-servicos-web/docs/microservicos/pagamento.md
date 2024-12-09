Microsserviço `Pagamento`

- Gerencia os pagamentos através da integração com um sistema externo de pagamento via Webhook.
- É necessário definir uma URL (isto é, um endpoint) que irá receber:
  - notificações de pagamento aprovado
  - notificações de pagamento recusado.
- Se o pagamento for aprovado, publicará o evento no tópico `Pagamentos_Aprovados`.
- Se o pagamento for recusado, publicará o evento no tópico `Pagamentos_Recusados`, para que o sistema cancele o pedido e atualize o estoque.