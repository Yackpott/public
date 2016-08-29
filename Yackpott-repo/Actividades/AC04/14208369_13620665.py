from AC04.py import *


def sonda():
    with open('sonda.txt', 'r') as f:

        dicc = {}
        for line in f:
            line = line.strip()
            line = line.split(',')

            tupla(line[0], line[1], line[2], line[3])

            dicc[tupla] = str(line[4])

        cordenadas = input("ingrese 4 cordenadas separada por comas")

        cordenadas = (cordenadas.split(','))

        for i in dicc:

            if cordenadas == i:
                print(dicc[i])

            else:
                print("no hay nada")


def traidores():
    traidores = Traidores("buffalos.txt", "rivales.txt")
    for i in traidores.traidores:
        print(i)


def pizzas():
    Pizzeria("pizzas.txt")


if __name__ == '__main__':
    exit_loop = False

    functions = {"1": sonda, "2": traidores, "3": pizzas}

    while not exit_loop:
        print(""" Elegir problema:
            1. Sonda
            2. Traidores
            3. Pizzas
            Cualquier otra cosa para salir
            Respuesta: """)

        user_entry = input()

        if user_entry in functions:
            functions[user_entry]()
        else:
            exit_loop = True
