from grafo import Grafo
from bfs import BFS
from doble import Doble
from ciclos import Ciclos
from flujo import Flujo
from nociclos import NoCiclos

cont = 0
grafo = Grafo()
print("El programa puede demorarse hasta dos minuto...")

# Probado con 1m y 10m y dan el mismo resultado
while cont < 1000000:
    grafo = grafo.agregar_nodo()
    cont += 1
f = open("red.txt", "w")
f.write(str(grafo))
f.close()
bfs = BFS(grafo)
f = open("rutaABummer.txt", "w")
f.write(str(bfs))
f.close()
doble = Doble(grafo)
f = open("rutasDobleSentido.txt", "w")
f.write(str(doble))
f.close()
ciclos = Ciclos(grafo)
f = open("ciclos.txt", "w")
f.write(str(ciclos))
f.close()
flujo = Flujo(grafo)
f = open("rutaMaxima.txt", "w")
f.write(str(flujo))
f.close()
no_ciclos = NoCiclos(grafo)
print("Listo")
