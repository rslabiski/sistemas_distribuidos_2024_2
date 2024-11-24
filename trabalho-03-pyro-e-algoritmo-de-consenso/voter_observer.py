from Pyro5.api import *
import sys

brokers_type = ['o', 'v']

if len(sys.argv) != 2 or sys.argv[1] not in brokers_type:
	sys.stderr.write(f'Usage: {sys.argv[0]} [v,o]\n')
	sys.exit(1)

class BrokerVoterObserver(object):

	state = None
	leader_uri = None
	log = []

	def __init__(self, state):
		try:
			self.daemon = Daemon()
			self.uri = self.daemon.register(self)
			print('Searching name server...')
			name_server = locate_ns()
			self.leader_uri = name_server.lookup('Lider_Epoca1')
			self.state = state
			Proxy(self.leader_uri).register_member(self.uri, self.state)
			print(f'Broker {self.state} URI: {self.uri} running...')

		except Exception as e:
			print(f'Error: {e}')
			sys.exit(1)	

	def run(self):
		try:
			print('Press Ctrl+C to shut down.')
			self.daemon.requestLoop()
		finally:
			self.cleanup()

	def cleanup(self):
		print("Shutting down...")
		self.daemon.shutdown()

	@expose
	@oneway
	def notify(self):
		try:
			print(f'Notified! Fetching...')
			data = Proxy(self.leader_uri).fetch(len(self.log))
			print(f'Received: {data}')
			for item in data:
				self.log.append(item)
			print(f'log = {self.log}')
		except Exception as e:
			print(f'Exception: {e}')

	@expose
	def commit_request(self):
		return True

broker = BrokerVoterObserver(sys.argv[1])
broker.run()