import signal
import grpc
import sqlite3
import hotel_group_pb2
import hotel_group_pb2_grpc
from concurrent import futures
from ports import HOTEL_GROUP_PORT

# Info do banco de dados
db_file = 'hotel_group_db.db'
table = 'quarto'

class ServiceImplementation(hotel_group_pb2_grpc.HotelGroupServicer):

    def bookRooms(self, request, context):
        try:
            data_base = sqlite3.connect(db_file)
            db_cursor = data_base.cursor()

            # Verifica ID e disponibilidade
            for room in request.rooms:
                db_cursor.execute(f'SELECT * FROM {table} WHERE id = {room.id}')
                result = db_cursor.fetchone()
                
                if not result:
                    print(f'Quarto ID {room.id} invalido')
                    return hotel_group_pb2.HotelGroupStatus(success=False)
                if result[1] < room.quantity:
                    print(f'{room.quantity} quarto(s) ID {room.id} indisponivel(is)')
                    return hotel_group_pb2.HotelGroupStatus(success=False)

            # Atualiza disponibilidade
            for room in request.rooms:
                query = f'UPDATE {table} SET quantidade = quantidade - {room.quantity} WHERE id = {room.id}'
                db_cursor.execute(query)
                print(f'Reservado(s) {room.quantity} quarto(s) ID {room.id}')
            
            data_base.commit()
            data_base.close()
            return hotel_group_pb2.HotelGroupStatus(success=True)
        
        except sqlite3.Error as err:
            print(f'ERR: {err}')
            return hotel_group_pb2.HotelGroupStatus(success=False)


    def cancelReservations(self, request, context):
        try:
            data_base = sqlite3.connect(db_file)
            db_cursor = data_base.cursor()

            # Verifica ID
            for room in request.rooms:
                db_cursor.execute(f'SELECT * FROM {table} WHERE id = {room.id}')
                result = db_cursor.fetchone()
                
                if not result:
                    print(f'Quarto ID {room.id} indisponivel para cancelamento')
                    return hotel_group_pb2.HotelGroupStatus(success=False)

            # Atualiza disponibilidade
            for room in request.rooms:
                query = f'UPDATE {table} SET quantidade = quantidade + {room.quantity} WHERE id = {room.id}'
                db_cursor.execute(query)
                print(f'Cancelado(s) {room.quantity} quarto(s) ID {room.id}')
            
            data_base.commit()
            data_base.close()
            return hotel_group_pb2.HotelGroupStatus(success=True)
        
        except sqlite3.Error as err:
            print(f'ERR: {err}')
            return hotel_group_pb2.HotelGroupStatus(success=False)


    def getRoomsAvailable(self, request, context):
        available_rooms = []
        try:
            data_base = sqlite3.connect(db_file)
            db_cursor = data_base.cursor()

            db_cursor.execute(f'SELECT * FROM {table}')
            rooms = db_cursor.fetchall()
            for room in rooms:
                available_rooms.append(hotel_group_pb2.Room(id=room[0], quantity=room[1]))

            data_base.close()

        except sqlite3.Error as err:
            print(f'ERR: {err}')

        return hotel_group_pb2.Rooms(rooms=available_rooms)


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