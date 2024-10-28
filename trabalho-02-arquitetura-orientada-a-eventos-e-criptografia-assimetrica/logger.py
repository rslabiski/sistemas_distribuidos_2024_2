import pika
import sys
import signal

topics = ['log.error.*', 'log.info.*', 'log.warning.*']

def callback_message(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")

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
    channel.exchange_declare(exchange='data', exchange_type='topic')
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    for topic in topics:
        channel.queue_bind(exchange='data', queue=queue_name, routing_key=topic)

    channel.basic_consume(queue=queue_name, on_message_callback=callback_message, auto_ack=True)
    print(' [*] Waiting for logs. To exit press CTRL+C')
    channel.start_consuming()

except pika.exceptions.AMQPConnectionError:
    sys.stderr.write("Error: Could not connect to RabbitMQ server.\n")
    sys.exit(1)

except Exception as e:
    sys.stderr.write(f"Unexpected error: {e}\n")
    sys.exit(1)