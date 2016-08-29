import random

"""
Eventos:
Se juega partido
Entra jugador

Variables de estados:
tiempo max
tiempo actual
cola jugadores
tiempo para el proximo partido
tiempo para el proximo jugador
"""


class Jugador:
    id = 0

    def __init__(self):
        self.habilidad = random.uniform(1, 10)
        self.jugadas = 0
        self.id = Jugador.id
        Jugador.id += 1


class Partido:

    def __init__(self, jugador1, jugador2):
        self.jugador1 = jugador1
        self.jugador1.jugadas += 1
        self.jugador2 = jugador2
        self.jugador2.jugadas += 1
        self.rand = random.random()
        if self.jugador1.habilidad / (self.jugador1.habilidad + self.jugador2.habilidad) < self.rand:
            self.perdedor = jugador1
            self.ganador = jugador2
        else:
            self.perdedor = jugador2
            self.ganador = jugador1


class Simulacion:

    def __init__(self, t_max):
        self.t_max = t_max
        self.t_actual = 0
        self.partido_actual = Partido(Jugador(), Jugador())
        self.jugadores = [Jugador()]
        self.t_partido = random.uniform(4, 6)
        self.t_jugador = random.expovariate(1 / 15)

    def run(self):
        print("Se inicio la simulacion")
        print("Entro el jugador 2 a la fila")
        while self.t_actual < self.t_max:
            if self.t_jugador <= self.t_partido:
                if self.t_actual + self.t_jugador > self.t_max:
                    print("Se acabo el tiempo")
                    break
                else:
                    jugador = Jugador()
                    self.jugadores.append(jugador)
                    self.t_partido -= self.t_jugador
                    self.t_actual += self.t_jugador
                    self.t_jugador = random.expovariate(1 / 15)
                    print("Entro un jugador {} a la fila".format(jugador.id))
            else:
                if self.t_actual + self.t_partido > self.t_max:
                    print("Se acabo el tiempo")
                    break
                else:
                    self.t_jugador -= self.t_partido
                    self.t_actual += self.t_partido
                    self.t_partido = random.uniform(4, 6)
                    print("El jugador {} le gano al jugador {}".format(
                        self.partido_actual.ganador.id, self.partido_actual.perdedor.id))
                    proba = 1 - (1 / 2)**self.partido_actual.perdedor.jugadas
                    if proba > random.random():
                        self.jugadores.append(self.partido_actual.perdedor)
                        print("El jugador {} reingresa a la cola".format(
                            self.partido_actual.perdedor.id))
                    else:
                        print(
                            "El jugador {} se retira".format(self.partido_actual.perdedor.id))
                    if len(self.jugadores) == 0:
                        print("No quedan jugadores en cola")
                        break
                    jugador_nuevo = self.jugadores.pop(0)
                    self.partido_actual = Partido(
                        self.partido_actual.ganador, jugador_nuevo)


t_max = 70
sim = Simulacion(t_max)
sim.run()
