#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import pickle
from datetime import datetime
from collections import defaultdict


class Persona:

    def __init__(self, id, nombre, amigos=[], favorito=""):
        self.id = id
        self.nombre = nombre
        self.amigos = amigos
        self.favorito = favorito
        self.guardados = 0
        self.t_guardado = None

    def agregar_amigo(self, amigo):
        self.amigos.append(amigo)

    def agregar_favorito(self, amigo):
        self.favorito = amigo

    def __getstate__(self):
        nueva = self.__dict__.copy()
        nueva.update({"guardados": self.guardados + 1})
        hoy = datetime.now()
        fecha = str(hoy.hour) + ":" + str(hoy.minute) + "-" + \
            str(hoy.day) + "-" + str(hoy.month) + "-" + str(hoy.year)
        nueva.update({"t_guardado": fecha})
        return nueva

    def __setstate__(self, state):
        self.__dict__ = state


def existe_persona(_id):
    aux = _id + ".iic2233"

    if aux in os.listdir("db"):
        return True
    else:
        return False


def get_persona(_id):
    if existe_persona(_id):
        with open('db/{}.iic2233'.format(_id), 'rb') as archivo:
            persona = pickle.load(archivo)
            return persona


def write_persona(persona):
    if not existe_persona(persona.id):
        with open('db/{}.iic2233'.format(persona.id), 'wb') as archivo:
            pickle.dump(persona, archivo)


def crear_persona(_id, nombre_completo):
    persona = Persona(_id, nombre_completo)
    write_persona(persona)


def agregar_amigo(id_1, id_2):

    persona_1 = get_persona(id_1)
    persona_2 = get_persona(id_2)

    if id_2 not in persona_1.amigos:
        persona_1.agregar_amigo(id_2)

    if id_1 not in persona_2.amigos:
        persona_2.agregar_amigo(id_1)

    with open('db/{}.iic2233'.format(persona_1.id), 'wb') as archivo:
        pickle.dump(persona_1, archivo)

    with open('db/{}.iic2233'.format(persona_2.id), 'wb') as archivo:
        pickle.dump(persona_2, archivo)


def set_persona_favorita(_id, id_favorito):
    if existe_persona(_id) and existe_persona(id_favorito):
        persona = get_persona(_id)
        persona.agregar_favorito(id_favorito)
        with open('db/{}.iic2233'.format(persona.id), 'wb') as archivo:
            pickle.dump(persona, archivo)


def get_persona_mas_favorita():
    lista = os.listdir("db")
    dicc = defaultdict(int)
    for archivo in lista:
        id = archivo.split(".")[0]
        persona = get_persona(id)
        if persona != None:
            dicc[persona.favorito] = dicc[persona.favorito] + 1

    aux = (None, 0)

    for k, v in dicc.items():
        if v > aux[1]:
            aux = (k, v)
    return aux


# ----------------------------------------------------- #
# Codigo para probar su tarea - No necesitan entenderlo #


def print_data(persona):
    if persona is None:
        print("[AVISO]: get_persona no está implementado")
        return

    for key, val in persona.__dict__.items():
        print("{} : {}".format(key, val))
    print("-" * 80)


# Metodo que sirve para crear el directorio db si no existia #

def make_dir():
    if not os.path.exists("./db"):
        os.makedirs("./db")


if __name__ == '__main__':
    make_dir()
    crear_persona("jecastro1", "Jaime Castro")
    crear_persona("bcsaldias", "Belen Saldias")
    crear_persona("kpb", "Karim Pichara")
    set_persona_favorita("jecastro1", "bcsaldias")
    set_persona_favorita("bcsaldias", "kpb")
    set_persona_favorita("kpb", "kpb")
    agregar_amigo("kpb", "jecastro1")
    agregar_amigo("kpb", "bcsaldias")
    agregar_amigo("jecastro1", "bcsaldias")

    jecastro1 = get_persona("jecastro1")
    bcsaldias = get_persona("bcsaldias")
    kpb = get_persona("kpb")

    print_data(jecastro1)
    print_data(bcsaldias)
    print_data(kpb)

    print(get_persona_mas_favorita())
