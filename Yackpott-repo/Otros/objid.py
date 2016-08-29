class clase:
	id = 0
	def __init__(self):
		clase.id += 1
		self.id = clase.id

clase1 = clase()
clase2 = clase()

print(clase1.id)
print(clase2.id)