from Pyro5.api import *
import sys

URI_size = 15

class Consumer(object):

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
		finish_loop = False
		while not finish_loop:
			try:
				offset = input('Type the offset (\'exit\' to finish): ')
				if offset == 'exit':
					finish_loop = True
				else:
					data = Proxy(self.lider_uri).get_message(int(offset))
					if data != None:
						print(f'Received: {data}')
					else:
						print(f'Without data!')
					
			except Exception as e:
				print(f'Exception: {e}')
				sys.exit(1)
	
	def cleanup(self):
		print("Shutting down...")
		self.daemon.shutdown()

consumer = Consumer()
consumer.run()