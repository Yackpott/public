class Reporte:

    def __init__(self, lista_pacientes):
        self.lista_pacientes = lista_pacientes

    def __iter__(self):
        return iter(self.lista_pacientes)

    def imp_color(self, color):
        return [i for i in self.lista_pacientes if i.color == color]


class Paciente:

    def __init__(self, id, ano, mes, dia, color, hora, motivo):
        self.id = id
        self.ano = ano
        self.mes = mes
        self.dia = dia
        self.color = color
        self.hora = hora
        self.motivo = motivo

    def __repr__(self):
        return "{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.id, self.ano,
                                                      self.mes, self.dia, self.color, self.hora, self.motivo)


def conteo():
    n = 0
    while True:
        yield n
        n += 1


def leer():
    cont = 1
    f = open("Reporte.txt", "r")
    print("Linea leida {}".format(cont))
    linea = f.readline()
    yield linea
    while linea != "":
        cont += 1
        print("Linea leida {}".format(cont))
        linea = f.readline()
        yield linea


def poblar():
    lista_amarillo = []
    lista_azul = []
    lista_naranja = []
    lista_rojo = []
    lista_verde = []
    gen = leer()
    linea = next(gen)
    contador = conteo()
    while len(lista_amarillo) < 10 or len(lista_azul) < 10 or len(lista_naranja) < 10 or len(lista_rojo) < 10 or len(lista_verde) < 10:
        linea = linea.split("\t")
        if linea[3] == "amarillo" and len(lista_amarillo) < 10:
            lista_amarillo.append(Paciente(next(contador), *linea))
        elif linea[3] == "azul" and len(lista_azul) < 10:
            lista_azul.append(Paciente(next(contador), *linea))
        elif linea[3] == "naranja" and len(lista_naranja) < 10:
            lista_naranja.append(Paciente(next(contador), *linea))
        elif linea[3] == "rojo" and len(lista_rojo) < 10:
            lista_rojo.append(Paciente(next(contador), *linea))
        elif linea[3] == "verde" and len(lista_verde) < 10:
            lista_verde.append(Paciente(next(contador), *linea))
        linea = next(gen)
    lista = []
    lista.extend(lista_amarillo)
    lista.extend(lista_azul)
    lista.extend(lista_naranja)
    lista.extend(lista_rojo)
    lista.extend(lista_verde)
    return Reporte(lista)

if __name__ == "__main__":
    reporte = poblar()
    print(reporte.imp_color("azul"))
