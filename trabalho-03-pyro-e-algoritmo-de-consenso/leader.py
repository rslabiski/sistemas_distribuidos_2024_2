import Pyro5.api
import sys

class BrokerLeader( object ):

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
	def publish(self, publisher_uri, message):
		total_votes = self.request_commit_all_quorum()
		if total_votes > len(self.quorum) / 2:
			self.log.append(message)
			print(f'\'{message}\' committed!')
			print(f'log = {self.log}')
			self.notify_all_quorum()
			Pyro5.api.Proxy(publisher_uri).committed(message)
		else:
			print(f'\'{message}\' uncommited!')
			Pyro5.api.Proxy(publisher_uri).uncommitted(message)
	
	@Pyro5.api.expose
	def fetch(self, offset):
		data = self.log[offset:]
		print(f'Fetched: {data}')
		return data
	
	def notify_all_quorum(self):
		for index, member in enumerate(self.quorum):
			try:
				print(f'Notifying V{index}...')
				Pyro5.api.Proxy(member).notify()
			except Pyro5.errors.CommunicationError as e:
				print(f'V{index} communication fail!')
			except Exception as e:
				print(f'{e}')
		print('Notifications completed!')
	
	def request_commit_all_quorum(self):
		total_commits = 0
		for index, member in enumerate(self.quorum):
			try:
				print(f'Requesting V{index} commit...')
				if Pyro5.api.Proxy(member).commit_request():
					total_commits += 1
			except Pyro5.errors.CommunicationError as e:
				print(f'V{index} communication fail!')
			except Exception as e:
				print(f'{e}')
		print(f'Total commits: {total_commits}')
		return total_commits

if __name__ == "__main__":
    leader = BrokerLeader()
    leader.run()