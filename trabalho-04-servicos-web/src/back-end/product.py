
keys = ['id', 'description', 'cost']

class Product:
	
	id = 0
	description = 'None Description'
	cost = 10.52

	def __init__(self, id, description, cost):
		self.id = id
		self.description = description
		self.cost = cost

	def __repr__(self):
		return f'ID: {self.id}\tcost: {self.cost}'