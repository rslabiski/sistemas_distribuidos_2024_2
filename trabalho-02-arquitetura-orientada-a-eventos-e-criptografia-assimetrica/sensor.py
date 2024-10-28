from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256
from Cryptodome.Signature import pkcs1_15
import pika
import sys

if len(sys.argv) < 4:
    sys.stderr.write(f'Usage: {sys.argv[0]} [temp/press] [log.error/log.info/log.warning/measure] [msg]...\n')
    sys.exit(1)

sensor_type = sys.argv[1]
topic = sys.argv[2]
message = sys.argv[3]

if ( sensor_type not in ['temp', 'press'] or 
     topic not in ['log.error', 'log.info', 'log.warning', 'measure'] or 
    (topic == 'measure' and not message.isnumeric())):
    
    sys.stderr.write(f'Usage: {sys.argv[0]} [temp/press] [log.error/log.info/log.warning/measure] [msg]...\n')
    sys.exit(1)

file_name = 'keys/Kt_priv.pem' if sensor_type == 'temp' else 'keys/Kp_priv.pem'
with open(file_name, "rb") as file:
    private_key = RSA.import_key(file.read())

hash_message = SHA256.new(message.encode('utf-8'))
signature = pkcs1_15.new(private_key).sign(hash_message)

# converte elementos para bytes para realizar a transmissao
full_message = f'{message}||{hash_message.hexdigest()}||{signature.hex()}'.encode('utf-8')
print(type(full_message))
topic = f'{topic}.{sensor_type}'

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='data', exchange_type='topic')
    channel.basic_publish(exchange='data', routing_key=topic, body = full_message)
    print(f'Sent {topic} {full_message}')
    connection.close()

except pika.exceptions.AMQPConnectionError:
    sys.stderr.write("Error: Could not connect to RabbitMQ server.\n")
    sys.exit(1)

except Exception as e:
    sys.stderr.write(f"Unexpected error: {e}\n")
    sys.exit(1)
