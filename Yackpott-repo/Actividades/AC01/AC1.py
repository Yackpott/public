

class Cielo:

        def __init__(self):
            self.lista_fields = []

        def agregar_field(self, field):
            self.lista_fields.append(field)


class Field:

    def __init__(self):
        self.lista_estrellas = []

    def agregar_estrellas(self, estrella):
        self.lista_estrellas.append(estrella)


class Estrella:

    def __init__(self, id, posicion):
        self.id = id
        self.posicion = posicion
        self.lista_obs = []

    def agregar_obs(self, obs):
        self.lista_obs.append(obs)

    def promedio_brillo(self):
        suma = 0
        for i in range(len(self.lista_obs)):
            suma += self.lista_obs[i].brillo
        return suma / len(self.lista_obs)

    def varianza_brillo(self):
        promedio = self.promedio_brillo()
        aux = 0
        for i in range(len(self.lista_obs)):
            aux += (self.lista_obs[i].brillo - promedio)**2
        return aux / len(self.lista_obs)


class Observacion:

    def __init__(self, tiempo, brillo, error):
        self.tiempo = tiempo
        self.brillo = brillo
        self.error = error

if __name__ == "__main__":
    cielo = Cielo()
    field_1 = Field()
    field_2 = Field()
    cielo.agregar_field(field_1)
    cielo.agregar_field(field_2)

    estrella_1 = Estrella(1, (1, 2))
    estrella_2 = Estrella(2, (1, 3))
    estrella_3 = Estrella(3, (1, 4))
    field_1.agregar_estrellas(estrella_1)
    field_1.agregar_estrellas(estrella_2)
    field_1.agregar_estrellas(estrella_3)

    estrella_4 = Estrella(4, (1, 5))
    estrella_5 = Estrella(5, (1, 6))
    estrella_6 = Estrella(6, (1, 7))
    field_2.agregar_estrellas(estrella_4)
    field_2.agregar_estrellas(estrella_5)
    field_2.agregar_estrellas(estrella_6)

    obs_1 = Observacion(15, 45, 2)
    obs_2 = Observacion(15, 45, 2)
    obs_3 = Observacion(15, 45, 2)
    obs_4 = Observacion(15, 45, 2)
    estrella_1.agregar_obs(obs_1)
    estrella_1.agregar_obs(obs_2)
    estrella_1.agregar_obs(obs_3)
    estrella_1.agregar_obs(obs_4)

    obs_5 = Observacion(15, 45, 2)
    obs_6 = Observacion(15, 45, 2)
    obs_7 = Observacion(15, 45, 2)
    obs_8 = Observacion(15, 45, 2)
    estrella_2.agregar_obs(obs_5)
    estrella_2.agregar_obs(obs_6)
    estrella_2.agregar_obs(obs_7)
    estrella_2.agregar_obs(obs_8)

    obs_9 = Observacion(15, 45, 2)
    obs_10 = Observacion(15, 45, 2)
    obs_11 = Observacion(15, 45, 2)
    obs_12 = Observacion(15, 45, 2)
    estrella_3.agregar_obs(obs_9)
    estrella_3.agregar_obs(obs_10)
    estrella_3.agregar_obs(obs_11)
    estrella_3.agregar_obs(obs_12)

    obs_13 = Observacion(15, 45, 2)
    obs_14 = Observacion(15, 45, 2)
    obs_15 = Observacion(15, 45, 2)
    obs_16 = Observacion(15, 45, 2)
    estrella_4.agregar_obs(obs_13)
    estrella_4.agregar_obs(obs_14)
    estrella_4.agregar_obs(obs_15)
    estrella_4.agregar_obs(obs_16)

    obs_17 = Observacion(15, 45, 2)
    obs_18 = Observacion(15, 45, 2)
    obs_19 = Observacion(15, 45, 2)
    obs_20 = Observacion(15, 45, 2)
    estrella_5.agregar_obs(obs_17)
    estrella_5.agregar_obs(obs_18)
    estrella_5.agregar_obs(obs_19)
    estrella_5.agregar_obs(obs_20)

    obs_21 = Observacion(15, 45, 2)
    obs_22 = Observacion(15, 45, 2)
    obs_23 = Observacion(15, 45, 2)
    obs_24 = Observacion(15, 45, 2)
    estrella_6.agregar_obs(obs_21)
    estrella_6.agregar_obs(obs_22)
    estrella_6.agregar_obs(obs_23)
    estrella_6.agregar_obs(obs_24)
