import math,random

class neurona:

	def __init__(self, dentritas, estimulos, infos, valores):
		self.respuestas = [0 for i in range(len(estimulos))]
		self.ponderados = []
		self.ponderadores = []
		self.estimulos = estimulos[:]
		cont = 0
		while len(self.estimulos)<dentritas:
			self.estimulos.append(self.estimulos[cont])
			cont+=1
		if dentritas<len(self.estimulos):
			self.estimulos = self.estimulos[0:dentritas]
		for i in range(dentritas):
			self.ponderadores.append(random.random())
		entrada()

	def entrada(self):
		for i in range(len(self.estimulos)):
			for k in range(len(self.infos)):
				if self.estimulos[i] == self.infos[k]:
					self.respuestas[i] = self.infos[k]
					break
		ponderacion()

	def ponderacion(self):
		for i in range(len(self.respuestas)):
			self.ponderadores[i] = self.respuestas[i]*self.ponderadores[i]
		nonlinear()
	
	def nonlinear(self):
		for i in self.ponderados:
			i = math.atanh(i)

	def salir(self):
		continue