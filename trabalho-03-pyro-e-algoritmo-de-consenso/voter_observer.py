import Pyro5.api
import sys

class BrokerVoterObserver(object):

	@Pyro5.server.expose
	def notify():
		return 'ACK'


# 3. Implemente o votante e o observador:
# 	sigam o código do cliente dos slides
# 	1.crie o daemon, pois vão receber notificação do
# 	  líder para buscar atualizações do tópico,
# 	  busquem a URI do "Lider_Epoca1" no serviço de nomes);

	def __init__(self, state):
		try:
			daemon = Pyro5.server.Daemon()				# cria um deamon Pyro
			uri = daemon.register(BrokerVoterObserver)	# cria um URI para o deamon Pyro
			name_server = Pyro5.api.locate_ns()			# localiza o servidor de nomes
			lider_uri = name_server.lookup('Lider_Epoca1') # localiza o URI do lider
			lider = Pyro5.api.Proxy(lider_uri) 			# cria o proxy para acessar os metodos do lider
			lider.register_member(uri, state)
			daemon.requestLoop()

		except Exception as e:
			print(f'Error: {e}')

def main():
	state = sys.argv[1]
	print(state)
	broker = BrokerVoterObserver(state)

if __name__ == "__main__":
	main()