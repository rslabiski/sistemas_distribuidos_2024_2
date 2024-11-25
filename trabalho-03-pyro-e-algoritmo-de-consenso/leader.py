from Pyro5.api import *
import Pyro5.errors
import time
import sys
import threading

stop_event = threading.Event()

def check_heart_beat(server):
	print('Check Heart beat thread running...')
	while not stop_event.is_set():
		server.check_quorum_heart_beat()
		time.sleep(float(server.heart_beat_timeout))
	print('Check Heart beat thread finished.')

class BrokerLeader( object ):

	name = 'Lider_Epoca1'
	log = []
	quorum = {} # dicionario com os membros do quórum (URI: tempo-do-ultimo-pulso)
	observers = [] # lista com os membros observadores (URI)

	def __init__(self):
		try:
			self.heart_beat_timeout = float(5)
			self.daemon = Daemon()
			self.uri = self.daemon.register(self)
			print(f'Leader URI: {self.uri}')
			print('Searching name server...')
			self.name_server = locate_ns()
			self.name_server.register(self.name, self.uri)
		except Exception as e:
			print(f'Exception: {e}')
			sys.exit(1)

	def run(self):
		try:
			print('Starting heartbeat thread...')
			self.pulse_thread = threading.Thread(target=check_heart_beat, args=(self,))
			self.pulse_thread.start()
			print('Press Ctrl+C to shut down.')
			self.daemon.requestLoop()
		finally:
			self.cleanup()

	def cleanup(self):
		try:
			stop_event.set()  # Sinaliza para a thread encerrar
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
		# atualiza o seu tempo no dicionario
		self.quorum[URI] = time.time()

	def check_quorum_heart_beat(self):
		print('Checking heart beat timeout...')
		members_to_remove = []
		for index, (member, value) in enumerate(self.quorum.items()):
			dt = time.time() - value
			if dt > self.heart_beat_timeout:
				members_to_remove.append(member)
				print(f'V{index} timeout!')
		# precisa remover no final para nao ocorrer problema no loop do dicionario
		for member in members_to_remove:
			print(f'URI {member} removed.')
			self.quorum.pop(member)
		
		# verifica promover observers
		if len(self.quorum) < 2 and len(self.observers):
			new_member = self.observers.pop()
			self.quorum[new_member] = time.time()
			Proxy(new_member).set_state('v')
			Proxy(new_member).notify()
			print(f'Observer {str(new_member)[:15]} promoted.')

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