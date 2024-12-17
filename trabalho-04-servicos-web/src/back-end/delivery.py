'''
Microsserviço `Entrega`

- O que faz:
  - emissão de notas
  - gerencia a entrega dos produtos
- Escuta em `Pagamentos_Aprovados`
- Publica em `Pedidos_Enviados`
'''

import pika
import sys
import signal
import json
import time
from common import *

def approved_payment(ch, method, properties, body):
	try:
		order = json.loads(body)
		order_id = order['order_id']
		print(f'[i] Order ID {order_id} issuing note...')
		time.sleep(2)
		print(f'[i] Note issued! Delivering...')
		time.sleep(2)
		ch.basic_publish(exchange=EXCHANGE, routing_key=PEDIDOS_ENVIADOS, body=json.dumps(order))
		print(f'[i] Order ID {order_id} Delivered!')
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
	channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=PAGAMENTOS_APROVADOS)
	channel.basic_consume(queue=queue_name, on_message_callback=approved_payment, auto_ack=True)

	print('[i] Waiting to send orders. To exit press CTRL+C')
	channel.start_consuming()

except pika.exceptions.AMQPConnectionError:
	sys.stderr.write("Error: Could not connect to RabbitMQ server.\n")
	sys.exit(1)

except Exception as e:
	sys.stderr.write(f"Unexpected error: {e}\n")
	sys.exit(1)