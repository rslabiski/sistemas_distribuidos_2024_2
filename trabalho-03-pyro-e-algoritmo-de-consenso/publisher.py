import Pyro5.api
import sys

if len(sys.argv) != 2:
    sys.stderr.write(f'Usage: {sys.argv[0]} \'message to publish\'\n')
    sys.exit(1)

try:
	message = sys.argv[1]
	name_server = Pyro5.api.locate_ns()			# localiza o servidor de nomes
	lider_uri = name_server.lookup('Lider_Epoca1') # localiza o URI do lider
	lider = Pyro5.api.Proxy(lider_uri) 			# cria o proxy para acessar os metodos do lider
	print( lider.publish(f'{message}') )

except Exception as e:
	print(f'Exception: {e}')