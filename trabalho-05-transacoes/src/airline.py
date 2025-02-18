import signal
import grpc
import sqlite3
import airline_pb2
import airline_pb2_grpc
from concurrent import futures
from ports import AIRLINE_PORT

# Info do banco de dados
db_file = 'airline_db.db'
table = 'passagem'

class ServiceImplementation(airline_pb2_grpc.AirlineServicer):

    def buyTickets(self, request, context):
        try:
            data_base = sqlite3.connect(db_file)
            db_cursor = data_base.cursor()

            # Verifica ID e estoque
            for ticket in request.tickets:
                db_cursor.execute(f'SELECT * FROM {table} WHERE id = {ticket.id}')
                result = db_cursor.fetchone()
                
                if not result:
                    print(f'Passagem ID {ticket.id} invalido')
                    return airline_pb2.AirlineStatus(success=False)
                if result[1] < ticket.quantity:
                    print(f'{ticket.quantity} passagem(s) ID {ticket.id} indisponivel(is)')
                    return airline_pb2.AirlineStatus(success=False)

            # Atualiza estoque
            for ticket in request.tickets:
                query = f'UPDATE {table} SET quantidade = quantidade - {ticket.quantity} WHERE id = {ticket.id}'
                db_cursor.execute(query)
                print(f'Comprada(s) {ticket.quantity} passagem(s) ID {ticket.id}')
            
            data_base.commit()
            data_base.close()
            return airline_pb2.AirlineStatus(success=True)
        
        except sqlite3.Error as err:
            print(f'ERR: {err}')
            return airline_pb2.AirlineStatus(success=False)


    def refoundTickets(self, request, context):
        try:
            data_base = sqlite3.connect(db_file)
            db_cursor = data_base.cursor()

            # Verifica ID
            for ticket in request.tickets:
                db_cursor.execute(f'SELECT * FROM {table} WHERE id = {ticket.id}')
                result = db_cursor.fetchone()
                if not result:
                    print(f'Passagem ID {ticket.id} indisponivel para estorno')
                    return airline_pb2.AirlineStatus(success=False)

            # Atualiza estoque
            for ticket in request.tickets:
                query = f'UPDATE {table} SET quantidade = quantidade + {ticket.quantity} WHERE id = {ticket.id}'
                db_cursor.execute(query)
                print(f'Estornada(s) {ticket.quantity} passagem(s) ID {ticket.id}')
            
            data_base.commit()
            data_base.close()
            return airline_pb2.AirlineStatus(success=True)
        
        except sqlite3.Error as err:
            print(f'ERR: {err}')
            return airline_pb2.AirlineStatus(success=False)


    def getTicketsAvailable(self, request, context):
        available_tickets = []
        try:
            data_base = sqlite3.connect(db_file)
            db_cursor = data_base.cursor()

            db_cursor.execute(f'SELECT * FROM {table}')
            tickets = db_cursor.fetchall()
            for ticket in tickets:
                available_tickets.append(airline_pb2.Ticket(id=ticket[0], quantity=ticket[1]))

            data_base.close()

        except sqlite3.Error as err:
            print(f'ERR: {err}')

        return airline_pb2.Tickets(tickets=available_tickets)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
airline_pb2_grpc.add_AirlineServicer_to_server(ServiceImplementation(), server)
server.add_insecure_port(f'[::]:{AIRLINE_PORT}')

def handle_signal(signum, frame):
    print("Encerrando...")
    server.stop(5) # Tempo de espera de 5 segundos para requisições em andamento

# Capturar sinais de interrupção (Ctrl+C ou kill)
signal.signal(signal.SIGINT, handle_signal)

if __name__ == "__main__":
    server.start()
    print(f'Companhia aerea executando na porta {AIRLINE_PORT}')
    server.wait_for_termination()  # Aguarda até receber Ctrl+C