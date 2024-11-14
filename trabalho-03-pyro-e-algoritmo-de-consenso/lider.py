import Pyro5.api

class BrokerLider(object):

	@Pyro5.server.expose
	def run(self):
		return 'hello from lider'

# 2. Implemente o líder (seguindo o código do servidor dos slides - crie uma instância do daemon, registre o objeto no daemon, registra o nome Lider_Epoca1 e a URI no serviço de nomes);
try:
	daemon = Pyro5.server.Daemon()				# cria um deamon Pyro
	uri = daemon.register(BrokerLider)				# cria um URI para o deamon Pyro
	name_server = Pyro5.api.locate_ns()			# localiza o servidor de nomes
	name_server.register('Lider_Epoca1', uri)	# registra o lider ao servidor de nomes
	print('registered on list name')			# retorno que esta funcionando
	daemon.requestLoop()						# executa o lider
except Exception as e:
	print(f'Error: {e}')