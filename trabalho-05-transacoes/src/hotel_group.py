import signal
import grpc
import hotel_group_pb2
import hotel_group_pb2_grpc
from concurrent import futures
from ports import HOTEL_GROUP_PORT

class ServiceImplementation(hotel_group_pb2_grpc.HotelGroupServicer):
    def book(self, request, context):
        print(f'book Received: {request}')
        return hotel_group_pb2.HotelGroupStatus(success=True)
    
    def cancelBook(self, request, context):
        print(f'cancelBook Received: {request}')
        return hotel_group_pb2.HotelGroupStatus(success=True)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
hotel_group_pb2_grpc.add_HotelGroupServicer_to_server(ServiceImplementation(), server)
server.add_insecure_port(f'[::]:{HOTEL_GROUP_PORT}')

def handle_signal(signum, frame):
    print("Shutting down...")
    server.stop(5) # Tempo de espera de 5 segundos para requisições em andamento

# Capturar sinais de interrupção (Ctrl+C ou kill)
signal.signal(signal.SIGINT, handle_signal)

if __name__ == "__main__":
    server.start()
    print(f'Hotel Group running on port {HOTEL_GROUP_PORT}')
    server.wait_for_termination()  # Aguarda até receber Ctrl+C