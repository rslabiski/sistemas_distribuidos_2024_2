# Tópico `Pedidos_Criados`
Mensagens serão consumidas pelos microsserviços Estoque e Pagamento (Descrição do microsserviço Principal).

| Subscribers   | Publishers  |
| :------------ | :---------- |
| `Notificação` | `Principal` |
| `Estoque`     |             |
| `Pagamento`   |             |

# Tópico `Pagamentos_Aprovados`
| Subscribers   | Publishers  |
| :------------ | :---------- |
| `Notificação` | `Pagamento` |
| `Entrega`     |             |
| `Principal`   |             |

# Tópico `Pagamentos_Recusados`
| Subscribers   | Publishers  |
| :------------ | :---------- |
| `Notificação` | `Pagamento` |
| `Principal`   |             |

# Tópico `Pedidos_Enviados`
| Subscribers   | Publishers |
| :------------ | :--------- |
| `Notificação` | `Entrega`  |
| `Principal`   |            |

# Tópico `Pedidos_Excluídos`
| Subscribers   | Publishers  |
| :------------ | :---------- |
| `Notificação` | `Principal` |
| `Estoque`     |             |