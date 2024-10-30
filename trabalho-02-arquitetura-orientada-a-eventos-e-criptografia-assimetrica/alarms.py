from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256
from Cryptodome.Signature import pkcs1_15
import pika
import sys
import signal

topics = ['measure.*']

def load_public_key(sensor_type):
    file_name = 'keys/Kt_pub.pub' if sensor_type == 'temp' else 'keys/Kp_pub.pub'
    with open(file_name, "rb") as file:
        return RSA.import_key(file.read())

def callback_message(ch, method, properties, body):
    try:
        # decomposição dos elementos
        topic = method.routing_key
        level, sensor_type = topic.split('.')[-2:]
        measure, hash_received, signature = body.decode('utf-8').split('||')
        
        if sensor_type not in  ['temp', 'press']:
            print(f'Invalid sensor type: {sensor_type}')
        else:
            hash_calculated = SHA256.new(measure.encode('utf-8'))

            if hash_calculated.hexdigest() != hash_received:
                print('Invalid hash!')
                print(f'Hash received: {hash_received}')
                print(f'Hash calculated: {hash_calculated}')
            else:
                public_key = load_public_key(sensor_type)
                pkcs1_15.new(public_key).verify(hash_calculated, bytes.fromhex(signature))
                print(f'Sensor type: {sensor_type}')
                print(f'Measure: {measure}\n')

    except Exception as err:
        print(f'Error on process message: {err}')


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