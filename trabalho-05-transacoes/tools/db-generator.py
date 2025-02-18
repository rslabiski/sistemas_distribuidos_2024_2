import sqlite3

try:
	generate = input('air | car | hotel: ')
	if generate == 'air':
		db_file = '../src/airline_db.db'
		table_name = 'passagem'
	elif generate == 'car':
		db_file = '../src/car_locator_db.db'
		table_name = 'carro'
	else:
		db_file = '../src/hotel_group_db.db'
		table_name = 'quarto'

	data_base = sqlite3.connect(db_file) # carrega/cria o banco de dados
	cursor = data_base.cursor()

	cursor.execute(f'CREATE TABLE {table_name} (id integer, quantidade integer)')
	cursor.execute(f'INSERT INTO {table_name} VALUES(0, 5)')
	cursor.execute(f'INSERT INTO {table_name} VALUES(1, 5)')
	cursor.execute(f'INSERT INTO {table_name} VALUES(2, 5)')
	cursor.execute(f'INSERT INTO {table_name} VALUES(3, 5)')
	cursor.execute(f'INSERT INTO {table_name} VALUES(4, 5)')

	data_base.commit() # Finalizar a transação
	data_base.close() # Fecha conexão com o banco
	print(f'Gerado banco {db_file} com tabela {table_name}')

except sqlite3.Error as err:
	print(err)