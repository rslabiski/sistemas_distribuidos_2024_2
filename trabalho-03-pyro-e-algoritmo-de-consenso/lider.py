import Pyro5.api
import sys

class BrokerLider( object ):

	name = 'Lider_Epoca1'
	log = []
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

	@Pyro5.api.expose
	def register_member(self, URI, state):
		if state == 'v':
			self.quorum.append(URI)
			print(f'{URI}: registered in quorum!')
		elif state == 'o':
			self.observers.append(URI)
			print(f'{URI}: registered in observer!')
		else:
			print('State unknown!')

	@Pyro5.api.expose
	@Pyro5.api.oneway
	@Pyro5.api.callback
	def publish(self, publisher_uri, message):
		self.log.append(message)
		print(f'log += {message}')
		self.notify_all_quorum()
		# total_votes = self.notify_all_quorum()
		# if total_votes > quorum/2
		Pyro5.api.Proxy(publisher_uri).uncommitted(message)
		# else
		# 		client.commit
	
	@Pyro5.api.expose
	@Pyro5.api.callback
	def fetch(self, offset):
		data = self.log[offset:]
		print(f'Buscado: {data}')
		return data
	
	def notify_all_quorum(self):
		i = 1
		print('Notificando quorum...')
		for member in self.quorum:
			try:
				print(f'notificando V{i}')
				i += 1
				Pyro5.api.Proxy(member).notify()
			except Exception as e:
				print(f'{e}')
		print('Terminado as notificações')

if __name__ == "__main__":
    lider = BrokerLider()
    lider.run()