import signal
import grpc
import airline_pb2
import airline_pb2_grpc
from concurrent import futures
from ports import AIRLINE_PORT

# Lista inicial de tickets
ticket_stock = {0:1, 1:2, 2:3, 3:4, 4:5, 5:6}

class ServiceImplementation(airline_pb2_grpc.AirlineServicer):

    def buyTickets(self, request, context):
        global ticket_stock
        # Verifica se há estoque suficiente
        for ticket in request.tickets:
            if ticket.id not in ticket_stock:
                print(f'ID {ticket.id} not available')
                return airline_pb2.AirlineStatus(success=False)
            if ticket_stock[ticket.id] < ticket.quantity:
                print(f'ID {ticket.id}, quantity {ticket.quantity} not available')
                return airline_pb2.AirlineStatus(success=False)
        # Atualiza estoque
        for ticket in request.tickets:
            ticket_stock[ticket.id] -= ticket.quantity
            print(f'Buy {ticket.quantity} ID {ticket.id}')
        
        return airline_pb2.AirlineStatus(success=True)
    
    def refoundTickets(self, request, context):
        global ticket_stock
        # Valida se os tickets existem no estoque
        for ticket in request.tickets:
            if ticket.id not in ticket_stock:
                print(f'ID {ticket.id} not available for refund')
                return airline_pb2.AirlineStatus(success=False)
        # Atualiza estoque
        for ticket in request.tickets:
            ticket_stock[ticket.id] += ticket.quantity
            print(f'Refound {ticket.quantity} ID {ticket.id}')
        return airline_pb2.AirlineStatus(success=True)
    
    def getTicketsAvailable(self, request, context):
        global ticket_stock
        available_tickets = [airline_pb2.Ticket(id=t_id, quantity=qty) for t_id, qty in ticket_stock.items()]
        return airline_pb2.Tickets(tickets=available_tickets)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
airline_pb2_grpc.add_AirlineServicer_to_server(ServiceImplementation(), server)
server.add_insecure_port(f'[::]:{AIRLINE_PORT}')

def handle_signal(signum, frame):
    print("Shutting down...")
    server.stop(5) # Tempo de espera de 5 segundos para requisições em andamento

# Capturar sinais de interrupção (Ctrl+C ou kill)
signal.signal(signal.SIGINT, handle_signal)

if __name__ == "__main__":
    server.start()
    print(f'Airline running on port {AIRLINE_PORT}')
    server.wait_for_termination()  # Aguarda até receber Ctrl+C