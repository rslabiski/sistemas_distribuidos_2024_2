from Pyro5.api import *
import sys

URI_size = 15

class Publisher(object):

	def __init__(self):
		try:
			self.daemon = Daemon()
			self.uri = self.daemon.register(self)
			print(f'URI: {str(self.uri)[:URI_size]}')
			print('Searching name server...')
			name_server = locate_ns()
			self.lider_uri = name_server.lookup('Lider_Epoca1')

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
				Proxy(self.lider_uri).publish(self.uri, f'{message}')
				print(f'Waiting committed/uncommitted...')
			except Exception as e:
				print(f'Exception: {e}')
				self.cleanup()

	@expose
	@oneway
	def committed(self, message):
		print(f'\'{message}\' committed!')
		self.next_publish()

	@expose
	@oneway
	def uncommitted(self, message):
		print(f'\'{message}\' uncommitted!')
		self.next_publish()

publisher = Publisher()
publisher.run()