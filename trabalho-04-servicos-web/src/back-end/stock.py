'''
Microsserviço `Estoque`

- O que faz:
	- gerencia estoque de produtos.
- Escuta em:
	- `Pedidos_Criados`
	- `Pedidos_Excluídos`
- Quando um pedido for criado, atualizar o estoque.
- Quando um pedido for excluído, atualizar o estoque.
- Quando um pagamento for recusado, atualizar o estoque.
- Responde requisições REST do microsserviço `Principal`, enviando dados dos produtos em estoque.
'''

from flask import Flask
import json
import pika
import sys
import time
import threading
from common import *

app = Flask(__name__)

stock_list = []
stock_list.append({'id':0, 'description':'banana'	,'cost': 1.25, 'amount': 100})
stock_list.append({'id':1, 'description':'pera'		,'cost': 0.75, 'amount': 100})
stock_list.append({'id':2, 'description':'morango'	,'cost': 5.00, 'amount': 100})
stock_list.append({'id':3, 'description':'melancia'	,'cost':10.00, 'amount': 100})
stock_list.append({'id':4, 'description':'tomate'	,'cost':14.00, 'amount': 100})
stock_list.append({'id':5, 'description':'abacate'	,'cost':15.00, 'amount': 100})

def print_stock():
	print('[i] Stock:')
	for item in stock_list:
		print(f"\t{item['amount']} {item['description']}")

def order_created(ch, method, properties, body):
	try:
		order = json.loads(body)
		order_id = order['order_id']
		print(f'[i] Order ID {order_id} created!')
		time.sleep(1)
		print(f'[i] Updating stock... (removendo elementos)')
		items = order['items']
		for item in items:
			item_id = item['id']
			stock_list[item_id]['amount'] = stock_list[item_id]['amount'] - item['amount']
		print_stock()
	except Exception as e:
		print(f'Exception: {e}')


def order_deleted(ch, method, properties, body):
	try:
		order = json.loads(body)
		order_id = order['order_id']
		print(f'[i] Order ID {order_id} deleted!')
		time.sleep(1)
		print(f'[i] Updating stock... (retornando os elementos)')
		items = order['items']
		for item in items:
			item_id = item['id']
			stock_list[item_id]['amount'] = stock_list[item_id]['amount'] + item['amount']
		print_stock()
	except Exception as e:
		print(f'Exception: {e}')


@app.get('/stock')
def get_products():
	return json.dumps(stock_list), 200


def run_stock():
	try:
		# Conectar ao servidor RabbitMQ
		connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
		channel = connection.channel()
		channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)

		# Vincular a fila e configurar consumidores específicos
		queue_name = channel.queue_declare('', exclusive=True).method.queue
		channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=PEDIDOS_CRIADOS)
		channel.basic_consume(queue=queue_name, on_message_callback=order_created, auto_ack=True)

		queue_name = channel.queue_declare('', exclusive=True).method.queue
		channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=PEDIDOS_EXCLUIDOS)
		channel.basic_consume(queue=queue_name, on_message_callback=order_deleted, auto_ack=True)

		print('[i] Stock control Running. To exit press CTRL+C')
		channel.start_consuming()

	except pika.exceptions.AMQPConnectionError:
		sys.stderr.write('Error: Could not connect to RabbitMQ server!')
		sys.exit(1)

	except Exception as e:
		sys.stderr.write(f'Exception: {e}\n')
		sys.exit(1)

if __name__ == '__main__':
	# Criar um thread para o consumir eventos dos tópicos do Rabbit
	threading.Thread(target=run_stock, daemon=True).start()
	app.run(host=HOST, port=PORT_STOCK)