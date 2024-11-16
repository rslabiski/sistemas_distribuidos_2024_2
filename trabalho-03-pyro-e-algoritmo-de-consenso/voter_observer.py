import Pyro5.api
import signal
import sys

brokers_type = ['o', 'v']

if len(sys.argv) != 2 or sys.argv[1] not in brokers_type:
	sys.stderr.write(f'Usage: {sys.argv[0]} [v,o]\n')
	sys.exit(1)

class BrokerVoterObserver(object):

	state = None

	def __init__(self, state):
		try:
			print('Searching name server...')
			name_server = Pyro5.api.locate_ns()		# localiza o servidor de nomes
			self.daemon = Pyro5.server.Daemon()				# cria um deamon Pyro
			self.uri = self.daemon.register(BrokerVoterObserver)		# cria um URI para o deamon Pyro
			lider_uri = name_server.lookup('Lider_Epoca1')	# localiza o URI do lider
			self.lider_proxy = Pyro5.api.Proxy(lider_uri) 			# cria o proxy para acessar os metodos do lider
			self.state = state
			self.lider_proxy.register_member(self.uri, self.state)
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

	@Pyro5.server.expose
	def notify(self, message):
		print(f'{message}')

if __name__ == "__main__":
    broker = BrokerVoterObserver(sys.argv[1])
    broker.run()