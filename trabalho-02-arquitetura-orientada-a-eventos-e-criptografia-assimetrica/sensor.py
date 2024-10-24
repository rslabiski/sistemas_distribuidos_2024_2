import pika
import sys

type = sys.argv[1]
topic = sys.argv[2]
msg = sys.argv[3]

if type not in ['temp', 'press']:
    sys.stderr.write('Usage, %s [temp/press] [topic] [msg]...\n' % sys.argv[0])
    sys.exit(1)


if topic not in ['log.error', 'log.info', 'log,warning', 'measure']:
    sys.stderr.write('Usage, %s [temp/press] [topic] [msg]...\n' % sys.argv[0])
    sys.exit(1)

if topic == 'measure' and not msg.isnumeric():
    sys.stderr.write('Usage, %s [temp/press] [topic] [msg]...\n' % sys.argv[0])
    sys.exit(1)

topic = topic + '.' + type


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='data', exchange_type='topic')

channel.basic_publish(exchange='data', routing_key=topic, body = msg)

print(f'Sent {topic} {msg}')
connection.close()
