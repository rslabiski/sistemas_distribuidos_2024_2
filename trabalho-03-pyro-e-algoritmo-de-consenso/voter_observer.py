import Pyro5.api
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
			self.daemon = Pyro5.server.Daemon()				# cria um deamon Pyro
			self.uri = self.daemon.register(self)			# cria um URI para o deamon Pyro
			print('Searching name server...')
			name_server = Pyro5.api.locate_ns()				# localiza o servidor de nomes
			self.leader_uri = name_server.lookup('Lider_Epoca1')	# localiza o URI do lider
			self.state = state
			Pyro5.api.Proxy(self.leader_uri).register_member(self.uri, self.state)
			print(f'Broker {self.state} URI: {self.uri} running...')

		except Exception as e:
			print(f'Error: {e}')
			sys.exit(1)	

	def run(self):
		try:
			print('Press Ctrl+C to shut down.')
			self.daemon.requestLoop()  # inicia o loop de requisições
		finally:
			self.cleanup()

	def cleanup(self):
		print("Shutting down...")
		self.daemon.shutdown()

	@Pyro5.api.expose
	@Pyro5.api.oneway
	def notify(self):
		try:
			print(f'Notified! Fetching...')
			data = Pyro5.api.Proxy(self.leader_uri).fetch(len(self.log))
			print(f'Received: {data}')
			for item in data:
				self.log.append(item)
			print(f'log = {self.log}')
		except Exception as e:
			print(f'Exception: {e}')

	@Pyro5.api.expose
	def commit_request(self):
		return True

broker = BrokerVoterObserver(sys.argv[1])
broker.run()