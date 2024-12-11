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
import common


def approved_payment(ch, method, properties, body):
	topic = common.approved_payments
	payload = 20
	channel.basic_publish(exchange=exchange, routing_key=topic, body=order_id)

	order_id = body.decode()
	print(f'[x] Processing approved payment for order: {order_id}')

def declined_payment(ch, method, properties, body):
	order_id = body.decode()
	print(f'[x] Processing declined payment for order: {order_id}')

def delivered(ch, method, properties, body):
	order_id = body.decode()
	print(f'[x] Processing delivered order: {order_id}')

def callback_finish(signal, frame):
	try:
		if connection.is_open:
			connection.close() 
			print(f'Connection closed\n')
	except Exception:
		pass # descarta erros de fechamento de conexão
	sys.exit(0)

try:
	# Sinal para finalizar programa
	signal.signal(signal.SIGINT, callback_finish)

	host = common.host
	exchange = common.exchange
	exchange_type = common.exchange_type

	# Conectar ao servidor RabbitMQ
	connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
	channel = connection.channel()
	channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)

	# Criar uma fila exclusiva para consumo
	result = channel.queue_declare('', exclusive=True)
	queue_name = result.method.queue

	# Vincular a fila e configurar consumidores específicos
	routing_key = common.approved_payments
	channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)
	channel.basic_consume(queue=queue_name, on_message_callback=approved_payment, auto_ack=True)

	routing_key = common.declined_payments
	channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)
	channel.basic_consume(queue=queue_name, on_message_callback=declined_payment, auto_ack=True)

	routing_key = common.delivered_orders
	channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)
	channel.basic_consume(queue=queue_name, on_message_callback=delivered, auto_ack=True)

	topic = common.created_orders
	order_id = 10
	channel.basic_publish(exchange=exchange, routing_key=topic, body=order_id)

	topic = common.deleted_orders
	order_id = 20
	channel.basic_publish(exchange=exchange, routing_key=topic, body=order_id)

	print('[x] Waiting for messages. To exit press CTRL+C')	
	channel.start_consuming()

except pika.exceptions.AMQPConnectionError:
	sys.stderr.write('Error: Could not connect to RabbitMQ server!')
	sys.exit(1)

except Exception as e:
	sys.stderr.write(f'Exception: {e}')
	sys.exit(1)