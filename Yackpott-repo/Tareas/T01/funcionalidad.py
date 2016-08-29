from curso import Curso, Horario, Evaluacion
from universidad import Alumno, Profesor


class Lector:

    def __init__(self, ruta):
        dicc = dict()
        self.lista_dicc = []
        self.archivo = open(ruta, "r", encoding="utf-8")
        leer = lambda: self.archivo.readline().replace("\"", "").replace(",\n", "").strip()
        linea = leer()
        linea = leer()
        while linea:
            var = linea[:linea.find(":")]
            if "}" in linea:
                self.lista_dicc.append(dicc)
                dicc = dict()
            elif "[" in linea and "]" not in linea:
                aux = []
                linea = leer()
                while "]" not in linea:
                    aux.append(linea)
                    linea = leer()
                dicc[var] = aux
            elif ":" in linea:
                dicc[var] = linea[linea.find(":") + 2:]
            linea = leer()
        self.archivo.close()


class LectorCursos(Lector):

    def __init__(self, ruta):
        super().__init__(ruta)
        for dicc in self.lista_dicc:
            if type(dicc["profesor"]) is list:
                aux = []
                for nombre in dicc["profesor"]:
                    nombre = nombre[nombre.find(" ") + 1:] + " " + nombre[:nombre.find(" ")]
                    aux.append(nombre)
                dicc["profesor"] = aux
            else:
                nombre = dicc["profesor"]
                dicc["profesor"] = nombre[
                    nombre.rfind(" ") + 1:] + " " + nombre[:nombre.rfind(" ")]
            cur = Curso(**dicc)
            for key, value in dicc.items():
                if "hora" in key:
                    if "cat" in key:
                        tipo = "catedra"
                        sala = dicc["sala_cat"]
                    elif "ayud" in key:
                        tipo = "ayudantia"
                        sala = dicc["sala_ayud"]
                    elif "lab" in key:
                        tipo = "laboratorio"
                        sala = dicc["sala_lab"]
                    horas = value[value.find(":") + 1:]
                    horas = horas.split(",")
                    dias = value[:value.find(":")]
                    dias = dias.split("-")
                    for dia in dias:
                        for hora in horas:
                            horario = Horario(tipo, dia, int(hora), sala)
                            cur.agregar_horario(horario)


class LectorEvaluaciones(Lector):

    def __init__(self, ruta):
        super().__init__(ruta)
        for dicc in self.lista_dicc:
            evaluacion = Evaluacion(**dicc)
            for cur in Curso.dicc_siglas[evaluacion.sigla]:
                if evaluacion.seccion in cur.seccion:
                    cur.agregar_evaluacion(evaluacion)


class LectorRequisitos(Lector):

    def __init__(self, ruta):
        super().__init__(ruta)
        for dicc in self.lista_dicc:
            for cur in Curso.dicc_siglas[dicc["sigla"]]:
                cur.agregar_requisitos(**dicc)


class LectorPersonas(Lector):

    def __init__(self, ruta):
        super().__init__(ruta)
        for dicc in self.lista_dicc:
            if dicc["alumno"] in "SI":
                Alumno(**dicc)
            else:
                Profesor(**dicc)
