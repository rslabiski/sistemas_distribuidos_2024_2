from Pyro5.api import *
import sys
import time
import threading

brokers_type = ['o', 'v']
URI_size = 15

if len(sys.argv) != 2 or sys.argv[1] not in brokers_type:
	sys.stderr.write(f'Usage: {sys.argv[0]} [v,o]\n')
	sys.exit(1)

stop_event = threading.Event()

def heart_beat(client):
	print('Heartbeat thread running...')
	while not stop_event.is_set():
		client.pulse()
		time.sleep(client.beat_time)
	print('Heartbeat thread finished.')

class BrokerVoterObserver(object):

	state = None
	leader_uri = None
	log_uncomitted = []
	log_comitted = []

	def __init__(self, state):
		try:
			self.beat_time = float(2)
			self.daemon = Daemon()
			self.uri = self.daemon.register(self)
			print('Searching name server...')
			name_server = locate_ns()
			self.leader_uri = name_server.lookup('Lider_Epoca1')
			self.state = state
			Proxy(self.leader_uri).register_member(self.uri, self.state)
			print(f'({self.state}) URI: {str(self.uri)[:URI_size]} running...')

		except Exception as e:
			print(f'Error: {e}')
			sys.exit(1)	

	def run(self):
		try:
			self.set_state(self.state)
			print('Press Ctrl+C to shut down.')
			self.daemon.requestLoop()
		finally:
			self.cleanup()

	def cleanup(self):
		print("Shutting down...")
		stop_event.set()  # Sinaliza para a thread encerrar
		self.daemon.shutdown()
		sys.exit(0)

	@expose
	@oneway
	def set_state(self, state):
		if state == 'v':
			print('Starting heartbeat thread...')
			self.pulse_thread = threading.Thread(target=heart_beat, args=(self,))
			self.pulse_thread.start()
			data = Proxy(self.leader_uri).get_message(0)
			self.log_uncomitted = data
			self.log_comitted = self.log_uncomitted
	
	
	def pulse(self):
		try:
			print(f'{str(self.uri)[:URI_size]} pulse')
			Proxy(self.leader_uri).beat(self.uri)
		except Exception as e:
			print(f'Pulse exception: {e}')
			self.cleanup()

	@expose
	@oneway
	def commit(self):
		self.log_comitted = self.log_uncomitted
		print(f'log_committed: {self.log_comitted}')

	@expose
	def notify(self):
		try:
			print(f'{str(self.uri)[:URI_size]} Notified! Fetching...')
			data = Proxy(self.leader_uri).fetch(len(self.log_uncomitted))
			print(f'Received: {data}')
			for item in data:
				self.log_uncomitted.append(item)
			print(f'log_uncomitted = {self.log_uncomitted}')
			return True
		except Exception as e:
			print(f'Exception: {e}')
			return False
	

broker = BrokerVoterObserver(sys.argv[1])
broker.run()