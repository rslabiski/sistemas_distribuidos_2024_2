import grpc
import airline_pb2
import airline_pb2_grpc
from ports import AIRLINE_PORT

def run():
    # Conectando ao servidor gRPC
    with grpc.insecure_channel(f'localhost:{AIRLINE_PORT}') as channel:
        stub = airline_pb2_grpc.AirlineStub(channel)

        # Criando uma requisição para comprar tickets
        tickets_request = airline_pb2.Tickets(
            tickets=[
                airline_pb2.Ticket(id=1, quantity=2),
                airline_pb2.Ticket(id=2, quantity=3)
            ]
        )

        # Chamando o método buyTickets
        print("Buying tickets...")
        buy_response = stub.buyTickets(tickets_request)
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
        refund_response = stub.refoundTickets(refund_request)
        print(f"Refund Response: {refund_response}")

if __name__ == "__main__":
    run()