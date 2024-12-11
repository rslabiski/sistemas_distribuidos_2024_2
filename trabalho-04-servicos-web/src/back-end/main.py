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
from flask import Flask, jsonify, request
import pika
import sys
import threading
from common import *

app = Flask(__name__)

def approved_payment(ch, method, properties, body):
	try:
		order_id = body.decode()
		print(f'[x] Processing approved payment for order: {order_id}')
	except Exception as e:
		print(f'[!] Error processing approved payment: {e}')


def declined_payment(ch, method, properties, body):
	try:
		order_id = body.decode()
		print(f'[x] Processing declined payment for order: {order_id}')
	except Exception as e:
		print(f'[!] Error processing declined payment: {e}')


def delivered(ch, method, properties, body):
	try:
		order_id = body.decode()
		print(f'[x] Processing delivered order: {order_id}')
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

		print('[x] Waiting for messages. To exit press CTRL+C')	
		channel.start_consuming()

	except pika.exceptions.AMQPConnectionError:
		sys.stderr.write('Error: Could not connect to RabbitMQ server!')
		sys.exit(1)

	except Exception as e:
		sys.stderr.write(f'Exception: {e}\n')
		sys.exit(1)


@app.get('/products')
def get_products():
	products = ['Product 1', 'Product 2', 'Product 3']
	return jsonify(products), 200

@app.post('/orders')
def create_order():
	data = request.get_json()
	print(data)
	order = { "client_id": 123,
		"items": [
			{"id": 1, "qnt": 10},
			{"id": 2, "qnt": 4},
			{"id": 3, "qnt": 5}
		]
	}
	order_id = {'order_id': 10}
	return jsonify(order_id), 201

if __name__ == '__main__':
	# Criar um thread para o consumir eventos dos tópicos do Rabbit
	threading.Thread(target=run_consumer, daemon=True).start()
	app.run(host=HOST, port=PORT_MAIN)