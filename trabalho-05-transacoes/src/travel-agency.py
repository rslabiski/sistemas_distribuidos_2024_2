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

        # Criando uma requisição para comprar tickets
        tickets_request = airline_pb2.Tickets(
            tickets=[
                airline_pb2.Ticket(id=1, quantity=2),
                airline_pb2.Ticket(id=2, quantity=3)
            ]
        )

        # Chamando o método buyTickets
        print("Buying tickets...")
        buy_response = airline_stub.buyTickets(tickets_request)
        print(f"Buy Response: {buy_response}")

        # Criando uma requisição para reembolsar tickets
        refund_request = airline_pb2.Tickets(
            tickets=[
                airline_pb2.Ticket(id=1, quantity=1),
                airline_pb2.Ticket(id=2, quantity=1)
            ]
        )

        # Chamando o método refoundTickets
        print("Refunding tickets...")
        refund_response = airline_stub.refoundTickets(refund_request)
        print(f"Refund Response: {refund_response}")

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