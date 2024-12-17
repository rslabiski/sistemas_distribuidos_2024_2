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
import signal
import time
import json
from common import *

def order_created(ch, method, properties, body):
	try:
		order = json.loads(body)
		order_id = order['order_id']
		approved = input(f'[?] Aprove Order ID {order_id}? s/n: ')
		print(f'[i] Processing...')
		time.sleep(1)
		if approved.lower() == 's':
			print(f'[+] Payment Order ID {order_id} Approved!\n')
			ch.basic_publish(exchange=EXCHANGE, routing_key=PAGAMENTOS_APROVADOS, body=json.dumps(order))
		else:
			print(f'[-] Payment Order ID {order_id} Refused!\n')
			ch.basic_publish(exchange=EXCHANGE, routing_key=PAGAMENTOS_RECUSADOS, body=json.dumps(order))
	except Exception as e:
		print(f'Exception: {e}')


def callback_finish(signal, frame):
	try:
		if connection.is_open:
			connection.close() 
			print(f'[i] Connection closed\n')
	except Exception:
		pass # descarta erros de fechamento de conexão
	sys.exit(0)

signal.signal(signal.SIGINT, callback_finish)


try:
	connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
	channel = connection.channel()
	channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)

	queue_name = channel.queue_declare('', exclusive=True).method.queue
	channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=PEDIDOS_CRIADOS)
	channel.basic_consume(queue=queue_name, on_message_callback=order_created, auto_ack=True)

	print('[i] Waiting orders. To exit press CTRL+C')
	channel.start_consuming()

except pika.exceptions.AMQPConnectionError:
	sys.stderr.write('Error: Could not connect to RabbitMQ server!')
	sys.exit(1)

except Exception as e:
	sys.stderr.write(f'Exception: {e}')
	sys.exit(1)