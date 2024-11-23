import Pyro5.api
import signal
import sys
import time

brokers_type = ['o', 'v']

if len(sys.argv) != 2 or sys.argv[1] not in brokers_type:
	sys.stderr.write(f'Usage: {sys.argv[0]} [v,o]\n')
	sys.exit(1)

class BrokerVoterObserver(object):

	state = None
	lider_uri = None
	log = []

	def __init__(self, state):
		try:
			self.daemon = Pyro5.server.Daemon()				# cria um deamon Pyro
			self.uri = self.daemon.register(self)			# cria um URI para o deamon Pyro
			print('Searching name server...')
			name_server = Pyro5.api.locate_ns()				# localiza o servidor de nomes
			self.lider_uri = name_server.lookup('Lider_Epoca1')	# localiza o URI do lider
			self.state = state
			Pyro5.api.Proxy(self.lider_uri).register_member(self.uri, self.state)
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
	@Pyro5.api.callback
	def notify(self):
		try:
			print(f'Notified!')
			print(f'Fetch...')
			data = Pyro5.api.Proxy(self.lider_uri).fetch(len(self.log))
			print(f'Received: {data}')
			self.log.append(data)
			print(f'log: {self.log}')
		except Exception as e:
			print(f'Error: {e}')

if __name__ == "__main__":
    broker = BrokerVoterObserver('v')
    broker.run()