import Pyro5.api
import sys

class BrokerLider( object ):

	name = 'Lider_Epoca1'
	quorum = [] # lista com os membros do quórum (URI: Proxy)
	observers = [] # lista com os membros observadores (URI: Proxy)

	def __init__(self):
		try:
			self.daemon = Pyro5.server.Daemon()
			self.uri = self.daemon.register(self)  # registra a instância da classe
			print('Searching name server...')
			self.name_server = Pyro5.api.locate_ns()  # localiza o servidor de nomes
			self.name_server.register(self.name, self.uri)  # registra o líder no servidor de nomes
			print(f'Leader URI: {self.uri}')
		except Exception as e:
			print(f'Exception: {e}')
			sys.exit(1)

	def run(self):
		try:
			print('Press Ctrl+C to shut down.')
			self.daemon.requestLoop()  # inicia o loop de requisições
		finally:
			self.cleanup()

	def cleanup(self):
		try:
			print('Removing from name server...')
			self.name_server.remove(self.name)
		except Exception as e:
			pass
		self.daemon.shutdown()

	@Pyro5.server.expose
	def register_member(self, URI, state):
		if state == 'v':
			self.quorum.append(URI)
			print(f'{URI}: registered in quorum!')
		elif state == 'o':
			self.observers.append(URI)
			print(f'{URI}: registered in observer!')
		else:
			print('State unknown!')

	@Pyro5.server.expose
	def publish(self, message):
		self.notify_all_quorum(message)
		return f'Published {message}'
	
	def notify_all_quorum(self, message):
		for member in self.quorum:
			try:
				Pyro5.api.Proxy(member).notify(message)
			except Exception as e:
				print(f'{e}')

if __name__ == "__main__":
    lider = BrokerLider()
    lider.run()