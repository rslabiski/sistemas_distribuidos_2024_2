import pika
import sys


topic = sys.argv[2]

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


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='data', exchange_type='topic')
result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange='data', queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
