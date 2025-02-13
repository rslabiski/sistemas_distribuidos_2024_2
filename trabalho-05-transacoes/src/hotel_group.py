import signal
import grpc
import hotel_group_pb2
import hotel_group_pb2_grpc
from concurrent import futures
from ports import HOTEL_GROUP_PORT

# Lista de quartos disponíveis
rooms_available = {0:3, 1:3, 2:3}

class ServiceImplementation(hotel_group_pb2_grpc.HotelGroupServicer):

    def bookRooms(self, request, context):
        global rooms_available
        # Verifica se há quartos disponiveis
        for room in request.rooms:
            if room.id not in rooms_available:
                print(f'Quarto ID {room.id} invalido')
                return hotel_group_pb2.HotelGroupStatus(success=False)
            if rooms_available[room.id] < room.quantity:
                print(f'{room.quantity} quartos ID {room.id} indisponiveis')
                return hotel_group_pb2.HotelGroupStatus(success=False)
        # Atualiza os quartos disponiveis
        for room in request.rooms:
            rooms_available[room.id] -= room.quantity
            print(f'Reservado(s) {room.quantity} quarto(s) ID {room.id}')
        return hotel_group_pb2.HotelGroupStatus(success=True)
    
    def cancelReservations(self, request, context):
        global rooms_available
        # Valida se os quartos foram reservados
        for room in request.rooms:
            if room.id not in rooms_available:
                print(f'Quarto ID {room.id} indisponivel para cancelamento')
                return hotel_group_pb2.HotelGroupStatus(success=False)
        # Atualiza estoque
        for room in request.rooms:
            rooms_available[room.id] += room.quantity
            print(f'Cancelado(s) {room.quantity} quarto(s) ID {room.id}')
        return hotel_group_pb2.HotelGroupStatus(success=True)
    
    def getRoomsAvailable(self, request, context):
        global rooms_available
        rooms_list = [hotel_group_pb2.Room(id=r_id, quantity=qty) for r_id, qty in rooms_available.items()]
        return hotel_group_pb2.Rooms(rooms=rooms_list)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
hotel_group_pb2_grpc.add_HotelGroupServicer_to_server(ServiceImplementation(), server)
server.add_insecure_port(f'[::]:{HOTEL_GROUP_PORT}')

def handle_signal(signum, frame):
    print("Encerrando...")
    server.stop(5) # Tempo de espera de 5 segundos para requisições em andamento

# Capturar sinais de interrupção (Ctrl+C ou kill)
signal.signal(signal.SIGINT, handle_signal)

if __name__ == "__main__":
    server.start()
    print(f'Rede hoteleira executando na porta {HOTEL_GROUP_PORT}')
    server.wait_for_termination()  # Aguarda até receber Ctrl+C