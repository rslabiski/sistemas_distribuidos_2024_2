import grpc
import airline_pb2
import airline_pb2_grpc
import car_locator_pb2_grpc
import car_locator_pb2
import hotel_group_pb2
import hotel_group_pb2_grpc
from ports import *

def run():
    # Conectando ao servidor gRPC
    with grpc.insecure_channel(f'localhost:{AIRLINE_PORT}') as airline_channel,\
        grpc.insecure_channel(f'localhost:{CAR_LOCATOR_PORT}') as car_locator_channel,\
        grpc.insecure_channel(f'localhost:{HOTEL_GROUP_PORT}') as hotel_group_channel:

        airline_stub = airline_pb2_grpc.AirlineStub(airline_channel)
        car_locator_stub = car_locator_pb2_grpc.CarLocatorStub(car_locator_channel)
        hotel_stub = hotel_group_pb2_grpc.HotelGroupStub(hotel_group_channel)

        # Etapa de compra de tickets
        available_tickets = airline_stub.getTicketsAvailable(airline_pb2.AirlineEmpty())
        print("Tickets disponíveis:")
        for ticket in available_tickets.tickets:
            print(f'\tTicket ID {ticket.id}: {ticket.quantity} disponiveis')
        
        user_input = input("Digite os IDs e quantidades desejadas (ex: 1 2 3 4 para 2 do ID 1 e 3 do ID 4): ")
        values = list(map(int, user_input.split()))
        if len(values) % 2 != 0:
            print("Entrada inválida. Certifique-se de inserir pares de valores (ID e quantidade).")
            return
        ticket_list = []
        for i in range(0, len(values), 2):
            ticket_list.append(airline_pb2.Ticket(id=values[i], quantity=values[i+1]))

        # Etapa de locação de carros
        available_cars = car_locator_stub.getCarsAvailable(car_locator_pb2.CarLocatorEmpty())
        print("Carros disponíveis:")
        for car in available_cars.cars:
            print(f'\tCarro ID {car.id}: {car.quantity} disponiveis')
       
        user_input = input("Digite os IDs e quantidades desejadas (ex: 1 2 3 4 para 2 do ID 1 e 3 do ID 4): ")
        values = list(map(int, user_input.split()))
        if len(values) % 2 != 0:
            print("Entrada inválida. Certifique-se de inserir pares de valores (ID e quantidade).")
            return
        car_list = []
        for i in range(0, len(values), 2):
            car_list.append(car_locator_pb2.Car(id=values[i], quantity=values[i+1]))

        # Etapa de reserva de quartos de hotel
        available_rooms = hotel_stub.getRoomsAvailable(hotel_group_pb2.HotelGroupEmpty())
        print("Quartos disponíveis:")
        for room in available_rooms.rooms:
            print(f'\tRoom ID {room.id}: {room.quantity} disponiveis')
        
        user_input = input("Digite os IDs e quantidades desejadas (ex: 1 2 3 4 para 2 do ID 1 e 3 do ID 4): ")
        values = list(map(int, user_input.split()))
        if len(values) % 2 != 0:
            print("Entrada inválida. Certifique-se de inserir pares de valores (ID e quantidade).")
            return
        rooms_list = []
        for i in range(0, len(values), 2):
            rooms_list.append(hotel_group_pb2.Room(id=values[i], quantity=values[i+1]))

        # Realizando a compra
        response = airline_stub.buyTickets(airline_pb2.Tickets(tickets=ticket_list))
        if not response.success:
            print("Falha na compra. Verifique a disponibilidade dos tickets.")
            return
        
        # Realizando a locação
        response = car_locator_stub.rentCars(car_locator_pb2.Cars(cars=car_list))
        if not response.success:
            print("Falha na locação. Verifique a disponibilidade dos carros.")
            print("Estornando passagens...")
            airline_stub.refoundTickets(airline_pb2.Tickets(tickets=ticket_list))
            return
        
        # Realizando a reserva
        response = hotel_stub.bookRooms(hotel_group_pb2.Rooms(rooms=rooms_list))
        if not response.success:
            print("Falha na Reserva. Verifique a disponibilidade dos quartos.")
            print("Estornando passagens...")
            airline_stub.refoundTickets(airline_pb2.Tickets(tickets=ticket_list))
            print("Cancelando alugueis dos carros...")
            car_locator_stub.cancelRent(car_locator_pb2.Cars(cars=car_list))
            return
        print("Sucesso!")

if __name__ == "__main__":
    run()