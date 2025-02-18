import signal
import grpc
import sqlite3
import car_locator_pb2
import car_locator_pb2_grpc
from concurrent import futures
from ports import CAR_LOCATOR_PORT

# Info do banco de dados
db_file = 'database/car_locator_db.db'
table = 'carro'

class ServiceImplementation(car_locator_pb2_grpc.CarLocatorServicer):

    def rentCars(self, request, context):
        try:
            data_base = sqlite3.connect(db_file)
            db_cursor = data_base.cursor()

            # Verifica ID e estoque
            for car in request.cars:
                db_cursor.execute(f'SELECT * FROM {table} WHERE id = {car.id}')
                result = db_cursor.fetchone()
                
                if not result:
                    print(f'Carro ID {car.id} invalido')
                    return car_locator_pb2.CarLocatorStatus(success=False)
                if result[1] < car.quantity:
                    print(f'{car.quantity} carro(s) ID {car.id} indisponivel(is)')
                    return car_locator_pb2.CarLocatorStatus(success=False)

            # Atualiza estoque
            for car in request.cars:
                query = f'UPDATE {table} SET quantidade = quantidade - {car.quantity} WHERE id = {car.id}'
                db_cursor.execute(query)
                print(f'Alugado(s) {car.quantity} carro(s) ID {car.id}')
            
            data_base.commit()
            data_base.close()
            return car_locator_pb2.CarLocatorStatus(success=True)
        
        except sqlite3.Error as err:
            print(f'ERR: {err}')
            return car_locator_pb2.CarLocatorStatus(success=False)


    def cancelRent(self, request, context):
        try:
            data_base = sqlite3.connect(db_file)
            db_cursor = data_base.cursor()

            # Verifica ID e estoque
            for car in request.cars:
                db_cursor.execute(f'SELECT * FROM {table} WHERE id = {car.id}')
                result = db_cursor.fetchone()
                if not result:
                    print(f'Carro ID {car.id} indisponivel para cancelamento')
                    return car_locator_pb2.CarLocatorStatus(success=False)

            # Atualiza estoque
            for car in request.cars:
                query = f'UPDATE {table} SET quantidade = quantidade + {car.quantity} WHERE id = {car.id}'
                db_cursor.execute(query)
                print(f'Cancelado(s) aluguel(is) de {car.quantity} carro(s) ID {car.id}')
            
            data_base.commit()
            data_base.close()
            return car_locator_pb2.CarLocatorStatus(success=True)
        
        except sqlite3.Error as err:
            print(f'ERR: {err}')
            return car_locator_pb2.CarLocatorStatus(success=False)


    def getCarsAvailable(self, request, context):
        available_cars = []
        try:
            data_base = sqlite3.connect(db_file)
            db_cursor = data_base.cursor()

            db_cursor.execute(f'SELECT * FROM {table}')
            cars = db_cursor.fetchall()
            for car in cars:
                available_cars.append(car_locator_pb2.Car(id=car[0], quantity=car[1]))

            data_base.close()

        except sqlite3.Error as err:
            print(f'ERR: {err}')

        return car_locator_pb2.Cars(cars=available_cars)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
car_locator_pb2_grpc.add_CarLocatorServicer_to_server(ServiceImplementation(), server)
server.add_insecure_port(f'[::]:{CAR_LOCATOR_PORT}')

def handle_signal(signum, frame):
    print("Encerrando...")
    server.stop(5) # Tempo de espera de 5 segundos para requisições em andamento

# Capturar sinais de interrupção (Ctrl+C ou kill)
signal.signal(signal.SIGINT, handle_signal)

if __name__ == "__main__":
    server.start()
    print(f'Locadora de carros executando na porta {CAR_LOCATOR_PORT}')
    server.wait_for_termination()  # Aguarda até receber Ctrl+C