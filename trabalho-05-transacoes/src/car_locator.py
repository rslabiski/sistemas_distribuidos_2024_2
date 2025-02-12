import signal
import grpc
import car_locator_pb2
import car_locator_pb2_grpc
from concurrent import futures
from ports import CAR_LOCATOR_PORT

class ServiceImplementation(car_locator_pb2_grpc.CarLocatorServicer):
    def rent(self, request, context):
        print(f'rent Received: {request}')
        return car_locator_pb2.CarLocatorStatus(success=True)
    
    def cancelRent(self, request, context):
        print(f'cancelRent Received: {request}')
        return car_locator_pb2.CarLocatorStatus(success=True)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
car_locator_pb2_grpc.add_CarLocatorServicer_to_server(ServiceImplementation(), server)
server.add_insecure_port(f'[::]:{CAR_LOCATOR_PORT}')

def handle_signal(signum, frame):
    print("Shutting down...")
    server.stop(5) # Tempo de espera de 5 segundos para requisições em andamento

# Capturar sinais de interrupção (Ctrl+C ou kill)
signal.signal(signal.SIGINT, handle_signal)

if __name__ == "__main__":
    server.start()
    print(f'Car locator running on port {CAR_LOCATOR_PORT}')
    server.wait_for_termination()  # Aguarda até receber Ctrl+C