class libro:
	id = 0

	def __init__(self, titulo, pags, topico, autor = None):
		self.titulo = titulo
		self.pags = pags
		self.topico = topico
		self.autor = autor
		self.id = libro.id
		libro.id += 1

class estante:
	id = 0

	def __init__(self, cant, topico):
		self.libros = []
		self.cant = cant
		self.topico = topico
		self.id = estante.id
		estante.id += 1

	def ordenar_por(self,atributo):
		sorted(self.libros[0], key=attrgetter(atributo))

	def agregar(self, *nuevos):
		agregar = True
		for nuevo in nuevos:
			for i in range(len(libros)):
				if libros[i] == nuevo:
					libros[i][1] += 1
					agregar = False
					break
			if agregar:
				libros.append([nuevo,1])
			agregar = True
	
	def imp(self):
		print(self.libros)

class libreria:
	def __init__(self):
		self.estantes = []

	def agregar(self, *estante):
		self.estantes.extend(estante)

	def imptopicos(self):
		aux = None
		for estante in self.estantes:
			if estante != aux:
				print(estante.topico)
				aux = estante

	def impest(self,estante):
		estante.imp()

est1 = estante(5,"Ciencia Ficcion")
est1.agregar(libro("addnj",34,"Ciencia Ficcion"),
	libro("kljo",98,"Ciencia Ficcion"),libro("klkl",101,"Ciencia Ficcion"),
	libro("cfttyf",2,"Ciencia Ficcion"),libro("buiui",31,"Ciencia Ficcion"))

est2 = estante(8,"Misterio")
est2.agregar(libro("addnj",34,"Misterio"),
	libro("kljo",98,"Misterio"),libro("klkl",101,"Misterio"),
	libro("cfttyf",2,"Misterio"),libro("buiui",31,"Misterio"))

est3 = estante(12,"Accion")
est3.agregar(libro("addnj",34,"Accion"),
	libro("kljo",98,"Accion"),libro("klkl",101,"Accion"),
	libro("cfttyf",2,"Accion"),libro("buiui",31,"Accion"))


libreria = libreria()
libreria.agregar(est1,est2,est3)


