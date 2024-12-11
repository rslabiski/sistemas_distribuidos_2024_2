'''
Microsserviço `Pagamento`

- Gerencia os pagamentos através da integração com um sistema externo de pagamento via Webhook.
- É necessário definir uma URL (isto é, um endpoint) que irá receber:
  - notificações de pagamento aprovado.
  - notificações de pagamento recusado.

- Se o pagamento for aprovado, publicará o evento no tópico `Pagamentos_Aprovados`.
- Se o pagamento for recusado, publicará o evento no tópico `Pagamentos_Recusados`.
'''

import pika
import sys
from common import *

try:
	connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
	channel = connection.channel()
	channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)

	payment = ''
	while payment != 'sair':
		payment = input('entre com aprovado/recusado/sair: ')
		if payment == 'aprovado':
			channel.basic_publish(exchange=EXCHANGE, routing_key=PAGAMENTOS_APROVADOS, body = '1234')
		elif payment == 'recusado':
			channel.basic_publish(exchange=EXCHANGE, routing_key=PAGAMENTOS_RECUSADOS, body = '4321')
		elif payment == 'sair':
			pass
		else:
			print(f'entrada invalida')

	connection.close()

except pika.exceptions.AMQPConnectionError:
	sys.stderr.write('Error: Could not connect to RabbitMQ server!')
	sys.exit(1)

except Exception as e:
	sys.stderr.write(f'Exception: {e}')
	sys.exit(1)