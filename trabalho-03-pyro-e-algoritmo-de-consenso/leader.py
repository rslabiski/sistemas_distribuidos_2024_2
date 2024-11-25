from Pyro5.api import *
import Pyro5.errors
import time
import sys
import threading

class BrokerLeader( object ):

	name = 'Lider_Epoca1'
	log = []
	quorum = {} # dicionario com os membros do quórum (URI: tempo-do-ultimo-pulso)
	observers = [] # lista com os membros observadores (URI)

	def __init__(self):
		try:
			self.daemon = Daemon()
			self.uri = self.daemon.register(self)
			print('Searching name server...')
			self.name_server = locate_ns()
			self.name_server.register(self.name, self.uri)
			print(f'Leader URI: {self.uri}')
		except Exception as e:
			print(f'Exception: {e}')
			sys.exit(1)

	def run(self):
		try:
			print('Press Ctrl+C to shut down.')
			self.daemon.requestLoop()
		finally:
			self.cleanup()

	def cleanup(self):
		try:
			print('Removing from name server...')
			self.name_server.remove(self.name)
		except Exception as e:
			pass
		self.daemon.shutdown()

	@expose
	def register_member(self, URI, state):
		if state == 'v':
			self.quorum[URI] = time.time()
			print(f'{URI}: registered in quorum!')
		elif state == 'o':
			self.observers.append(URI)
			print(f'{URI}: registered in observer!')
		else:
			print('State unknown!')

	@expose
	@oneway
	def beat(self, URI):
		self.quorum[URI] = time.time()
		for index, (key, value) in enumerate(self.quorum.items()):
			if URI == key:
				print(f'V{index} -: {value:.4f}')
			else:
				print(f'V{index}  : {value:.4f}')

	@expose
	@oneway
	def publish(self, publisher_uri, message):
		print(f'Commit request: \'{message}\'')
		total_commits = 1 + self.request_commit_all_quorum()
		print(f'Total commits: {total_commits}')
		if total_commits > len(self.quorum) / 2:
			self.log.append(message)
			print(f'\'{message}\' committed!')
			print(f'log = {self.log}')
			self.notify_all_quorum()
			Proxy(publisher_uri).committed(message)
		else:
			print(f'\'{message}\' uncommitted!')
			Proxy(publisher_uri).uncommitted(message)
	
	@expose
	def fetch(self, offset):
		data = self.log[offset:]
		print(f'Fetched: {data}')
		return data
	
	def notify_all_quorum(self):
		for index, (member, value) in enumerate(self.quorum.items()):
			try:
				print(f'Notifying V{index}...')
				Proxy(member).notify()
			except Pyro5.errors.CommunicationError as e:
				print(f'V{index} communication fail!')
			except Exception as e:
				print(f'{e}')
		print('Notifications completed!')
	
	def request_commit_all_quorum(self):
		total_commits = 0
		for index, (member, value) in enumerate(self.quorum.items()):
			try:
				print(f'Requesting V{index} commit...')
				if Proxy(member).commit_request():
					total_commits += 1
			except Pyro5.errors.CommunicationError as e:
				print(f'V{index} communication fail!')
			except Exception as e:
				print(f'{e}')
		return total_commits

leader = BrokerLeader()
leader.run()