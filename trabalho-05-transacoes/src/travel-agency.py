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

        # Obtendo a lista de tickets disponíveis
        available_tickets = airline_stub.getTicketsAvailable(airline_pb2.AirlineEmpty())
        
        # Exibindo a lista de tickets ao usuário
        print("Tickets disponíveis:")
        for ticket in available_tickets.tickets:
            print(f'ID: {ticket.id}, Quantidade: {ticket.quantity}')
        
        # Solicitando entrada do usuário
        user_input = input("Digite os IDs e quantidades desejadas (ex: 1 2 3 4 para 2 do ID 1 e 3 do ID 4): ")
        
        # Convertendo entrada para lista de tickets
        values = list(map(int, user_input.split()))
        if len(values) % 2 != 0:
            print("Entrada inválida. Certifique-se de inserir pares de valores (ID e quantidade).")
            return
        
        ticket_list = []
        for i in range(0, len(values), 2):
            ticket_list.append(airline_pb2.Ticket(id=values[i], quantity=values[i+1]))
        
        # Realizando a compra
        response = airline_stub.buyTickets(airline_pb2.Tickets(tickets=ticket_list))
        
        # Exibindo o resultado
        if not response.success:
            print("Falha na compra. Verifique a disponibilidade dos tickets.")
            return

        # Criando uma requisição para alugar carro
        car = car_locator_pb2.Car(id=1)

        print("Renting a car...")
        rent_response = car_locator_stub.rent(car)
        print(f"Rent Response: {rent_response}")

        # Cancelando aluguel de carro
        print(f'Canceling car rental...')
        status = car_locator_stub.cancelRent(car)
        print(f'Cancel status: {status}')

        # Criando uma requisição para reservar quarto
        room = hotel_group_pb2.Room(id=1)

        print(f'Booking a room...')
        book_response = hotel_stub.book(room)
        print(f'Book Response: {book_response}')

        print(f'Canceling room booking..')
        status = hotel_stub.cancelBook(room)
        print(f'Cancel status: {status}')

if __name__ == "__main__":
    run()