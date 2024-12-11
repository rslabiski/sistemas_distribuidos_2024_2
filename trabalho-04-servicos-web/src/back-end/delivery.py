'''
Microsserviço `Entrega`

- Gerencia:
  - emissão de notas
  - entrega dos produtos
- Consome eventos do tópico `Pagamentos_Aprovados`
- Publica no tópico `Pedidos_Enviados`
'''

import pika
import sys
import signal
from common import *

def approved_payment(ch, method, properties, body):
    try:
        order_id = str(10)
        print(f'[x] Payment order id {order_id} approved! Delivering...')
        ch.basic_publish(exchange=EXCHANGE, routing_key=PEDIDOS_ENVIADOS, body = order_id)
    except Exception as e:
        print(f'Exception: {e}')

def callback_finish(signal, frame):
    try:
        if connection.is_open:
            connection.close() 
            print(f'Connection closed\n')
    except Exception:
        pass # descarta erros de fechamento de conexão
    sys.exit(0)

signal.signal(signal.SIGINT, callback_finish)

try:
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)

	queue_name = channel.queue_declare('', exclusive=True).method.queue
	channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=PAGAMENTOS_APROVADOS)
	channel.basic_consume(queue=queue_name, on_message_callback=approved_payment, auto_ack=True)

	print(' [*] Waiting to send orders. To exit press CTRL+C')
	channel.start_consuming()

except pika.exceptions.AMQPConnectionError:
	sys.stderr.write("Error: Could not connect to RabbitMQ server.\n")
	sys.exit(1)

except Exception as e:
	sys.stderr.write(f"Unexpected error: {e}\n")
	sys.exit(1)