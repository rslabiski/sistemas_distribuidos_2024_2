import signal
import grpc
import car_locator_pb2
import car_locator_pb2_grpc
from concurrent import futures
from ports import CAR_LOCATOR_PORT

# Lista inicial de carros
car_stock = {0:5, 1:5, 2:5, 3:5}

class ServiceImplementation(car_locator_pb2_grpc.CarLocatorServicer):

    def rentCars(self, request, context):
        global car_stock
        # Verifica se há estoque suficiente
        for car in request.cars:
            if car.id not in car_stock:
                print(f'Carro ID {car.id} invalido')
                return car_locator_pb2.CarLocatorStatus(success=False)
            if car_stock[car.id] < car.quantity:
                print(f'{car.quantity} carros ID {car.id} indisponiveis')
                return car_locator_pb2.CarLocatorStatus(success=False)
        # Atualiza estoque
        for car in request.cars:
            car_stock[car.id] -= car.quantity
            print(f'Alugado(s) {car.quantity} carro(s) ID {car.id}')
        return car_locator_pb2.CarLocatorStatus(success=True)
    
    def cancelRent(self, request, context):
        global car_stock
        # Valida se os carros existem no estoque
        for car in request.cars:
            if car.id not in car_stock:
                print(f'Carro ID {car.id} indisponivel para cancelamento')
                return car_locator_pb2.CarLocatorStatus(success=False)
        # Atualiza estoque
        for car in request.cars:
            car_stock[car.id] += car.quantity
            print(f'Cancelado(s) aluguel(is) de {car.quantity} carro(s) ID {car.id}')
        return car_locator_pb2.CarLocatorStatus(success=True)
    
    def getCarsAvailable(self, request, context):
        global car_stock
        available_cars = [car_locator_pb2.Car(id=c_id, quantity=qty) for c_id, qty in car_stock.items()]
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