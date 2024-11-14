import Pyro5.api

class BrokerLider(object):

	# 2. Implemente o líder (seguindo o código do servidor dos slides - crie uma instância do daemon, registre o objeto no daemon, registra o nome Lider_Epoca1 e a URI no serviço de nomes);
	
	quorum = {}													# dicionário com os membros do quórum, URI : estado	

	def __init__(self):
		try:
			self.daemon = Pyro5.server.Daemon()					# cria um deamon Pyro
			self.uri = self.daemon.register(type(self))			# cria um URI para o deamon Pyro
			name_server = Pyro5.api.locate_ns()					# localiza o servidor de nomes
			name_server.register('Lider_Epoca1', self.uri)		# registra o lider ao servidor de nomes
			print('registered on list name')					# retorno que esta funcionando
			self.daemon.requestLoop()							# executa o lider
		except Exception as e:
			print(f'Error: {e}')


	@Pyro5.server.expose
	def run(self):
		return 'hello from lider'

	@Pyro5.server.expose
	def register_member(self, URI, state):
		self.quorum[URI] = state
		print(f'{URI}: {state} registered in quorum!')	
	
	def print_quorum(self):
		for URI, state in self.quorum.items():
			print(f'URI: {URI}	State: {state}')

def main():
	lider = BrokerLider()
	lider.print_quorum()

if __name__ == "__main__":
	main()