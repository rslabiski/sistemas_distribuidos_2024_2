import pika
import sys

if len(sys.argv) < 4:
    sys.stderr.write(f'Usage: {sys.argv[0]} [temp/press] [log.error/log.info/log.warning/measure] [msg]...\n')
    sys.exit(1)

type = sys.argv[1]
topic = sys.argv[2]
msg = sys.argv[3]

if ( type not in ['temp', 'press'] or 
     topic not in ['log.error', 'log.info', 'log.warning', 'measure'] or 
    (topic == 'measure' and not msg.isnumeric())):
    
    sys.stderr.write(f'Usage: {sys.argv[0]} [temp/press] [log.error/log.info/log.warning/measure] [msg]...\n')
    sys.exit(1)

topic = topic + '.' + type

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='data', exchange_type='topic')
    channel.basic_publish(exchange='data', routing_key=topic, body = msg)
    print(f'Sent {topic} {msg}')
    connection.close()

except pika.exceptions.AMQPConnectionError:
    sys.stderr.write("Error: Could not connect to RabbitMQ server.\n")
    sys.exit(1)

except Exception as e:
    sys.stderr.write(f"Unexpected error: {e}\n")
    sys.exit(1)
