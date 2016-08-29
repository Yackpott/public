from maritimos import Barco, Guerra, Lancha, Puerto
from aereos import Explorador, IXXI, Caza
from mapa import Mapa
from sistema import Sistema
from radar import Radar
from estadisticas import Estadisticas
from copy import copy


n = 15
lista_1 = [Barco(), Guerra(), Lancha(), Puerto(), Explorador(), IXXI(), Caza()]
lista_2 = [Barco(), Guerra(), Lancha(), Puerto(), Explorador(), IXXI(), Caza()]

# input si es Oponente o computador
player = "Jugador"
otro = "Oponente"

mapa_1 = Mapa(player, n)
mapa_2 = Mapa(otro, n)

radar_1 = Radar()
radar_2 = Radar()

estadisticas_1 = Estadisticas(player, otro)
estadisticas_2 = Estadisticas(otro, player)

def leer(texto):
        aux = input(texto)
        exit(0) if aux == "exit" else None
        return aux


def mapear(mapa, lista):
    lista = copy(lista)
    while len(lista) > 0:
        vehiculo = None
        while not vehiculo:
            vehiculo = elegir(mapa, lista)
        while True:
            linea = leer("Ingrese coordenada del primer punto de la forma x,y: ")
            if mapa.agregar(vehiculo, linea):
                break


def elegir(mapa, lista):
    try:
        imp = ""
        for i in range(len(lista)):
            imp += "{} --> {}\n".format(str(i),
                                        lista[i].__class__.__name__)
        print("Mapa del {}".format(mapa.tipo))
        linea = leer("{} ingrese vehiculo a agregar:\n".format(mapa.tipo) + imp)
        return lista.pop(int(linea))
    except Exception as e:
        print("[ERROR] {}".format(type(e).__name__))
    return None

"""mapear(mapa_1, lista_1)
mapear(mapa_2, lista_2)"""

sistema_1 = Sistema(player, mapa_1, mapa_2, lista_1, lista_2, radar_1, estadisticas_1, estadisticas_2, n)
sistema_2 = Sistema(otro, mapa_2, mapa_1, lista_2, lista_1, radar_2, estadisticas_2, estadisticas_1, n)


aux1 = copy(lista_1)
aux2 = ["0,1", "3,3", "6,6", "9,9", "12,12", "0,0", "4,4", "8,8"]
aux3 = copy(lista_2)
aux4 = ["0,1", "3,3", "6,6", "9,9", "12,12", "0,0", "4,4", "8,8"]

for i in aux1:
    for j in aux2:
        mapa_1.agregar(i, j)
        aux2.pop(0)
        break

for i in aux3:
    for j in aux4:
        mapa_2.agregar(i, j)
        aux4.pop(0)
        break

print(mapa_1)
print(mapa_2)


while True:
    sistema_1.turno()
    sistema_2.turno()
# Se terminara el proceso con un exit(0) desde sistema
