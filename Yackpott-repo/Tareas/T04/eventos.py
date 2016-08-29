from collections import deque
import random


class Evento:
    cola = deque()


class Incendio(Evento):
    pass


class Robo(Evento):
    pass


class Enfermo(Evento):
    pass


class Taxi(Evento):
    pass
