import signal
import grpc
import airline_pb2
import airline_pb2_grpc
from concurrent import futures
from ports import AIRLINE_PORT

class ServiceImplementation(airline_pb2_grpc.AirlineServicer):
    def buyTickets(self, request, context):
        print(f'buyTickets Received: {request}')
        return airline_pb2.Status(success=True)
    
    def refoundTickets(self, request, context):
        print(f'refoundTickets Received: {request}')
        return airline_pb2.Status(success=True)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
airline_pb2_grpc.add_AirlineServicer_to_server(ServiceImplementation(), server)
server.add_insecure_port(f'[::]:{AIRLINE_PORT}')

def handle_signal(signum, frame):
    print("Shutting down...")
    server.stop(5) # Tempo de espera de 5 segundos para requisições em andamento

# Capturar sinais de interrupção (Ctrl+C ou kill)
signal.signal(signal.SIGINT, handle_signal)

if __name__ == "__main__":
    server.start()
    print(f'Airline running on port {AIRLINE_PORT}')
    server.wait_for_termination()  # Aguarda até receber Ctrl+C