import Pyro5.api
import sys

class Publisher(object):

	def __init__(self):
		try:
			self.daemon = Pyro5.server.Daemon()				# cria um deamon Pyro
			self.uri = self.daemon.register(self)			# cria um URI para o deamon Pyro
			print(f'URI: {self.uri}')
			print('Searching name server...')
			name_server = Pyro5.api.locate_ns()			# localiza o servidor de nomes
			self.lider_uri = name_server.lookup('Lider_Epoca1') # localiza o URI do lider

		except Exception as e:
			print(f'Exception: {e}')
			sys.exit(1)
	
	def run(self):
		try:
			self.next_publish()
			self.daemon.requestLoop()  # inicia o loop de requisições
		except Exception as e:
			print(f'Exception: {e}')
			sys.exit(1)
	
	def cleanup(self):
		print("Shutting down...")
		self.daemon.shutdown()

	def next_publish(self):
		message = input('Type new publish (\'exit\' to finish): ')
		if message == 'exit':
			self.cleanup()
		else:
			try:
				print(f'Request to publish \'{message}\'...')
				Pyro5.api.Proxy(self.lider_uri).publish(self.uri, f'{message}')
				print(f'Waiting committed/uncommitted...')
			except Exception as e:
				print(f'Exception: {e}')
				self.cleanup()

	@Pyro5.api.expose
	@Pyro5.api.oneway
	def committed(self, message):
		print(f'\'{message}\' committed!')
		self.next_publish()

	@Pyro5.api.expose
	@Pyro5.api.oneway
	def uncommitted(self, message):
		print(f'\'{message}\' uncommitted!')
		self.next_publish()

publisher = Publisher()
publisher.run()