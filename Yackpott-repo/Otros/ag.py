import random

class Nodo:
	def __init__(self, Nombre="", X=0, Y = 0, Nodo=None):
		if Nodo is None:
			self.Nombre = Nombre
			self.X = X
			self.Y = Y
		else:
			self.Nombre = Nodo.Nombre
			self.X = Nodo.X
			self.Y = Nodo.Y
		self.Padre = None

def GenerarPoblacion(puntos, distancia):
	rango = 10 ** distancia - 1
	nodos = []
	poblacion = []
	for i in range(puntos):
		nombre = i + 1
		x = random.randint(-rango,rango)
		y = random.randint(-rango,rango)
		nodo = Nodo(Nombre=nombre, X=x, Y=y)
		nodos.append(nodo)
	GenerarArbol(nodos, poblacion)
	return poblacion

def GenerarArbol(nodos, poblacion, raiz = None):
	if len(nodos)>0:
		random.shuffle(nodos)
		for nodo in nodos:
			faltantes = nodos[:]
			faltantes.remove(nodo)
			hijo = Nodo(Nodo = nodo)
			hijo.Padre = raiz
			GenerarArbol(faltantes, poblacion, hijo)
	else:
			n = raiz
			solucion = []
			while n is not None:
				solucion.append(n)
				n = n.Padre
			solucion.reverse()
			poblacion.append(solucion)

def CalcularRuta(solucion):
	total = 0
	for i in range(len(solucion)-1):
		x1 = solucion[i].X
		x2 = solucion[i+1].X
		y1 = solucion[i].Y
		y2 = solucion[i+1].Y
		total += ((x2-x1)**2+(y2-y1)**2)**0.5
	return total

if __name__ == '__main__':
	puntos = int(input("Ingrese numero de puntos: "))
	distancia = int(input("Ingrese la distancia: "))
	poblacion = GenerarPoblacion(puntos, distancia)
	for solucion in poblacion:
		string = "["
		for nodo in solucion:
			string += str(nodo.Nombre) + " "
		print(string[:len(string)-1] + "] " + str(CalcularRuta(solucion)))
	for nodo in poblacion[0]:
		print(str(nodo.Nombre) + " X=" + str(nodo.X) + " Y=" + str(nodo.Y))