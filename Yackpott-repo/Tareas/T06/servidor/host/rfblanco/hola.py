import pickle


class Archivo:

    def __init__(self, ruta):
        with open(ruta, "r") as arch:
            self.file = arch.read()

ar = Archivo("02-11-15.txt")
pick = pickle.dumps(ar)


def agregar_largo(pick):
    return (len(pick)).to_bytes(4, byteorder='big') + pick

byte = agregar_largo(pick)


def obtener_largo(byte):
    return int.from_bytes(byte[:4], byteorder='big')
