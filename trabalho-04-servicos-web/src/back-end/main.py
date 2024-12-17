'''
- API REST
- Recebe requisições REST do frontend para:
  - visualizar produtos 			/products GET
  - inserir produtos do carrinho	/orders/products PUT
  - atualizar produtos do carrinho	/orders/products/<id> PATCH
  - remover produtos do carrinho	/orders/products/<id> DELETE
  - realizar pedidos				/orders POST
  - excluir pedidos					/orders/<id> DELETE
  - consultar pedidos.				/orders GET
- Publica em `Pedidos_Criados`
- Publica em `Pedidos_Excluídos`
- Se inscreve em `Pagamentos_Aprovados`
- Se inscreve em `Pagamentos_Recusados`
- Se inscreve em `Pedidos_Enviados`
- Cada novo pedido recebido será publicado no tópico `Pedidos_Criados`
- Atualiza o status de cada pedido de acordo com o evento de tópico inscrito
- `!` O principal usa o rest_get para o Estoque para visualizar os produtos disponíveis
- Quando um cliente excluir um pedido, publica no tópico `Pedidos_Excluídos`.
- Quando o pagamento de um pedido for recusado, publica no tópico `Pedidos_Excluídos`.
'''
from flask import Flask, request
import json
import requests
import pika
import sys
import time
import threading
from common import *

app = Flask(__name__)

orders = []

def set_order_status(id, status):
	orders[id]['status'] = status
	print(f"[i] Order ID {orders[id]['order_id']}: {orders[id]['status']}")

def approved_payment(ch, method, properties, body):
	try:
		order = json.loads(body)
		order_id = order['order_id']
		print(f"[i] Processing approved payment for order ID {order_id}...")
		time.sleep(2)
		set_order_status(order_id, 'payment-approved')
	except Exception as e:
		print(f'[!] Error processing approved payment: {e}')


def declined_payment(ch, method, properties, body):
	try:
		order = json.loads(body)
		order_id = order['order_id']
		print(f'[i] Processing declined payment for order ID {order_id}')
		time.sleep(2)
		set_order_status(order_id, 'payment-refused')
		connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
		channel = connection.channel()
		channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)
		channel.basic_publish(exchange=EXCHANGE, routing_key=PEDIDOS_EXCLUIDOS, body=json.dumps(order))
	except Exception as e:
		print(f'[!] Error processing declined payment: {e}')


def delivered(ch, method, properties, body):
	try:
		order = json.loads(body)
		order_id = order['order_id']
		print(f'[i] Processing delivery for order ID {order_id}')
		time.sleep(2)
		set_order_status(order_id, 'delivered')
	except Exception as e:
		print(f'[!] Error processing delivered order: {e}')


def run_consumer():
	try:
		# Conectar ao servidor RabbitMQ
		connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
		channel = connection.channel()
		channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)

		# Vincular a fila e configurar consumidores específicos
		queue_name = channel.queue_declare('', exclusive=True).method.queue
		channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=PAGAMENTOS_APROVADOS)
		channel.basic_consume(queue=queue_name, on_message_callback=approved_payment, auto_ack=True)

		queue_name = channel.queue_declare('', exclusive=True).method.queue
		channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=PAGAMENTOS_RECUSADOS)
		channel.basic_consume(queue=queue_name, on_message_callback=declined_payment, auto_ack=True)

		queue_name = channel.queue_declare('', exclusive=True).method.queue
		channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=PEDIDOS_ENVIADOS)
		channel.basic_consume(queue=queue_name, on_message_callback=delivered, auto_ack=True)

		print('[i] Waiting for messages. To exit press CTRL+C')	
		channel.start_consuming()

	except pika.exceptions.AMQPConnectionError:
		sys.stderr.write('Error: Could not connect to RabbitMQ server!')
		sys.exit(1)

	except Exception as e:
		sys.stderr.write(f'Exception: {e}\n')
		sys.exit(1)


@app.get('/products')
def get_products():
	try:
		stock_url = f"http://{HOST}:{PORT_STOCK}/stock"
		response = requests.get(stock_url)
		return response.json(), response.status_code
	except Exception as e:
		sys.stderr.write(f'Exception: {e}\n')
		return json.dumps('Server Error!'), 500
	
'''
Formato:
{
	"items": [
		{"id": 1, "amount": 10},
		{"id": 2, "amount": 4},
		{"id": 3, "amount": 5}
	]
}
'''
@app.post('/orders')
def create_order():
	try:
		order = request.get_json()
		order['order_id'] = len(orders)
		order['status'] = 'payment_pending'
		connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
		channel = connection.channel()
		channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)
		channel.basic_publish(exchange=EXCHANGE, routing_key=PEDIDOS_CRIADOS, body=json.dumps(order))
		orders.append(order)
		print(f"[+] Created Order ID {order['order_id']} ({order['status']})")
		return order, 201
	except Exception as e:
		sys.stderr.write(f'Exception: {e}\n')
		return json.dumps('Server Error!'), 500

if __name__ == '__main__':
	# Criar um thread para o consumir eventos dos tópicos do Rabbit
	threading.Thread(target=run_consumer, daemon=True).start()
	app.run(host=HOST, port=PORT_MAIN)