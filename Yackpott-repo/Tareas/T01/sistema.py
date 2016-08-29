import os.path
import numpy as np
from datetime import datetime
from curso import Curso
from universidad import Universidad, Profesor


class Sistema:

    def __init__(self, usuario):
        self.usuario = usuario
        if os.path.isfile("bkn.txt"):
            texto = """Ingrese:
        1 --> para cargar calcula grupos
        2 --> para para calcular grupos\n"""
            linea = input(texto)
            while linea != "1" and linea != "2":
                if linea == "exit":
                    exit(0)
                linea = input(texto)
            if linea == "1":
                self.cargar_grupos()
            elif linea == "2":
                self.calcular_grupos()
        else:
            self.calcular_grupos()

    def calcular_grupos(self):
        print("Calculando bacanosidad, puedo tomar unos minutos")
        self.alumnos = []
        for persona in Universidad.dicc_personas.values():
            if persona.alumno:
                self.alumnos.append(persona)
        self.alumnos = sorted(self.alumnos, key=lambda alumno: alumno.nombre)
        dim = len(self.alumnos)
        mat = np.zeros((dim, dim))
        for i in range(dim):
            for j in range(dim):
                if self.alumnos[j].nombre in self.alumnos[i].idolos:
                    mat[i][j] = 1 / len(self.alumnos[i].idolos)
        for i in range(50):
            mat = np.dot(mat, mat)
        for j in range(dim):
            self.alumnos[j].agregar_bkn(mat[0][j])
        self.alumnos = sorted(
            self.alumnos, key=lambda alumno: alumno.bkn, reverse=True)
        f = open("bkn.txt", "w")
        for i in range(dim):
            aux = int((i // (dim / 10)) + 1)
            self.alumnos[i].agregar_grupo(aux)
            relativa = self.alumnos[i].bkn / self.alumnos[0].bkn
            self.alumnos[i].agregar_relativa(relativa)
            f.write(self.alumnos[i].usuario + ";" + str(self.alumnos[i].grupo) + ";" + str(self.alumnos[i].relativa) + "\n")
        f.close()

    def cargar_grupos(self):
        f = open("bkn.txt", "r")
        linea = f.readline().strip("\n")
        while linea != "":
            usuario, grupo, relativa = linea.split(";")
            Universidad.dicc_personas[usuario].grupo = int(grupo)
            Universidad.dicc_personas[usuario].agregar_relativa(float(relativa))
            linea = f.readline().strip("\n")
        f.close()

    def existe_ramo(self, nrc):
        if nrc in Curso.dicc_nrc:
            return True
        else:
            print("No existe ese ramo... ")
            return False

    def no_inscrito(self, usuario, nrc):
        if Curso.dicc_nrc[nrc] in Universidad.dicc_personas[usuario].lista_ramos:
            return False
        else:
            return True

    def cumple_requisitos(self, usuario, nrc):
        if (usuario, nrc) in Profesor.lista_permisos:
            return True
        if "NO" in Curso.dicc_nrc[nrc].aprobacion:
            if "No tiene" in Curso.dicc_nrc[nrc].requisitos:
                return True
            req = Curso.dicc_nrc[nrc].requisitos
            req = req.replace("(c)", "c")
            lista = Universidad.dicc_personas[usuario].curso_aprobados.copy()
            cursos_tomar = Universidad.dicc_personas[usuario].lista_ramos.copy()
            try:
                for sigla in lista:
                    aux = Curso.dicc_siglas[sigla][0].equivalencias
                    if "No tiene" in aux:
                        continue
                    aux = aux.replace(" ", "").replace("(", "").replace(")", "")
                    aux = aux.split("o")
                    lista.extend(aux)
            except:
                pass
            for curso in cursos_tomar:
                lista.append(curso.sigla + "c")
            if self.rec(req, lista):
                return True
        print("No cumple requisitos... ")
        return False

    def ind(self, req):
        aux = 0
        cont = 0
        for letra in req:
            if letra == "(":
                aux += 1
            elif letra == ")":
                aux -= 1
            if aux == 0 and cont > req.find("("):
                return cont
            cont += 1

    def rec(self, req, lista):
        req = req.replace(" ", "")
        if req.count("(") == 0:
            if req.find("o") >= 0:
                req = req.split("o")
                for i in req:
                    for j in lista:
                        if i == j or i.replace("c", "") == j:
                            return True
                return False
            else:
                req = req.split("y")
                for i in range(len(lista)):
                    for j in range(len(req)):
                        if lista[i] == req[j] or req[j].replace("c", "") == lista[i]:
                            req.pop(j)
                            i = 0
                            j -= 1
                            break
                if len(req) == 0:
                    return True
                else:
                    return False
        else:
            resto = req
            resto = req[:req.find("(")] + req[self.ind(req) + 1:]
            req = req[req.find("(") + 1: self.ind(req)]
            if resto.find("o") < resto.find("y") or resto.find("y") == -1:
                return self.rec(resto, lista) or self.rec(req, lista)
            else:
                return self.rec(resto, lista) and self.rec(req, lista)


class Bummer(Sistema):

    def __init__(self, usuario):
        super().__init__(usuario)
        self.es_hora()
        opciones = {
            "1": self.inscribir_ramo,
            "2": self.botar_ramo,
            "3": self.imprimir_horario,
            "4": self.guardar_horario,
            "5": self.guardar_evaluaciones,
        }
        while True:
            linea = input("""Ingrese:
        1 --> para inscribir ramo
        2 --> para botar ramo
        3 --> para imprimir horario
        4 --> para guardar horario
        5 --> para guardar evaluaciones
        atras --> para ir atras(solo si creditos>=30)\n""")
            if linea == "exit":
                exit(0)
            if linea == "atras" and Universidad.dicc_personas[self.usuario].creditos>=30:
                break
            elif linea == "atras":
                print("Tienes menos de 30 creditos... ")
                continue
            try:
                opciones[linea]()
            except:
                print("Error intente nuevamente... ")

    def es_hora(self):
        linea = input("Ingrese hora con forma 23:55 por ejemplo...: ")
        if linea == "exit":
            exit(0)
        try:
            hora = datetime.strptime(linea, '%H:%M')
        except:
            print("Error... ")
            return self.es_hora()
        horario = Universidad.dicc_personas[self.usuario].horario
        if hora > datetime.strptime(horario.inicio, '%H:%M') and hora < datetime.strptime(horario.fin, '%H:%M'):
            self.hora = True
        else:
            print("Fuera de horario... ")
            return self.es_hora()

    def no_topes(self, nrc):
        for ramo in Universidad.dicc_personas[self.usuario].lista_ramos:
            for horario in ramo.horarios:
                if "catedra" in horario.tipo or "laboratorio" in horario.tipo:
                    for nuevo in Curso.dicc_nrc[nrc].horarios:
                        if "catedra" in nuevo.tipo or "laboratorio" in nuevo.tipo:
                            if horario.dia == nuevo.dia and horario.hora == nuevo.hora:
                                print("Error tope...")
                                return False
                            if ramo.campus != Curso.dicc_nrc[nrc].campus and \
                            horario.dia == nuevo.dia and abs(horario.hora - nuevo.hora) <= 1:
                                print("Error campus...")
                                return False
            for evaluacion in ramo.evaluaciones:
                for otro in Curso.dicc_nrc[nrc].evaluaciones:
                    if evaluacion.fecha == otro.fecha:
                        print("Error evaluacion...")
                        return False
        return True

    def inscribir_ramo(self):
        if self.hora:
            nrc = input("Ingrese codigo nrc a agregar: ")
            if self.existe_ramo(nrc):
                if self.no_inscrito(self.usuario, nrc):
                    if self.cumple_requisitos(self.usuario, nrc):
                        if Curso.dicc_nrc[nrc].vacantes > 0:
                            if Universidad.dicc_personas[self.usuario].creditos <=\
                             Universidad.dicc_personas[self.usuario].max_creditos:
                                if self.no_topes(nrc):
                                    Universidad.dicc_personas[self.usuario].agregar_ramo(Curso.dicc_nrc[nrc])
                                    Universidad.dicc_personas[self.usuario].creditos += Curso.dicc_nrc[nrc].creditos
                                    Curso.dicc_nrc[nrc].agregar_alumno(Universidad.dicc_personas[self.usuario])
                                    Curso.dicc_nrc[nrc].vacantes -= 1
                                    print("Agregado exitosamente... ")
                            else:
                                print("Excediste el limite de creditos... ")
                        else:
                            print("No hay vacantes... ")
                else:
                    print("Ya estaba inscrito")

    def botar_ramo(self, nrc=None):
        if self.hora:
            nrc = input("Ingrese codigo nrc a botar: ")
            if self.existe_ramo(nrc):
                if not self.no_inscrito(self.usuario, nrc):
                    Universidad.dicc_personas[self.usuario].botar_ramo(Curso.dicc_nrc[nrc])
                    Universidad.dicc_personas[self.usuario].creditos -= Curso.dicc_nrc[nrc].creditos
                    Curso.dicc_nrc[nrc].eliminar_alumno(self.usuario)
                    Curso.dicc_nrc[nrc].vacantes += 1
                    print("Borrado existosamente... ")
                else:
                    print("No estaba inscrito")

    def imprimir_horario(self):
        print("Imprimiendo ramos... \n\n")
        for ramo in Universidad.dicc_personas[self.usuario].lista_ramos:
            print(ramo.sigla + "-" + ramo.seccion + str(ramo.horarios) + "\n\n")

    def guardar_horario(self):
        f = open("horario.txt", "w")
        for ramo in Universidad.dicc_personas[self.usuario].lista_ramos:
            f.write(ramo.sigla + "-" + ramo.seccion + str(ramo.horarios) + "\n\n")
        f.close()
        print("Guardado como horario.txt ...\n")

    def guardar_evaluaciones(self):
        f = open("prueba.txt", "w")
        for ramo in Universidad.dicc_personas[self.usuario].lista_ramos:
            f.write(str(ramo.evaluaciones))
        f.close()
        print("Guardado como prueba.txt ...\n")


class Pacmatico(Sistema):
    dicc_ramos = dict()

    def __init__(self, usuario):
        super().__init__(usuario)
        for ramo in Curso.dicc_nrc:
            Pacmatico.dicc_ramos[ramo] = []
        b = Universidad.dicc_personas[usuario].relativa
        self.cont = 0
        cred = Universidad.dicc_personas[usuario].creditos_aprobados
        self.puntos = (1+b/4+cred/4000)*800
        self.puntos_antiguo = self.puntos
        opciones = {
            "1": self.ver_apuestas,
            "2": self.agregar_ramo,
            "3": self.borrar_ramo,
            "4": self.agregar_apuesta,
            "5": self.resultados
        }
        while True:
            linea = input("""Ingrese:
        1 --> para ver apuestas
        2 --> para agregar ramo
        3 --> para borrar ramo
        4 --> para agregar apuestas
        5 --> para obtener resultado de los ramos
        atras --> para ir atras\n""")
            if linea == "exit":
                exit(0)
            if linea == "atras":
                break
            if linea == "5":
                self.resultados()
                break
            try:
                opciones[linea]()
            except:
                print("Error intente nuevamente... ")

    def ver_apuestas(self):
        aux = True
        for apuestas in Pacmatico.dicc_ramos.values():
            for i in range(len(apuestas)):
                if apuestas[i].usuario == self.usuario:
                    print(apuestas[i])
                    aux = False
        if aux:
            print("No tienes ramos para imprimir")

    def agregar_ramo(self):
        nrc = input("Ingrese codigo nrc a agregar: ")
        if self.existe_ramo(nrc):
            if self.no_inscrito(self.usuario, nrc):
                if self.cumple_requisitos(self.usuario, nrc):
                    self.cont += 1
                    Universidad.dicc_personas[self.usuario].agregar_ramo(Curso.dicc_nrc[nrc])
                    Universidad.dicc_personas[self.usuario].creditos += Curso.dicc_nrc[nrc].creditos
                    ap = Apuesta(self.usuario, nrc, self.puntos)
                    Pacmatico.dicc_ramos[nrc].append(ap)
                    print("Se agrego el ramo satisfactoriamente")
            else:
                print("Ya estaba inscrito")

    def borrar_ramo(self):
        nrc = input("Ingrese codigo nrc a borrar: ")
        if self.existe_ramo(nrc):
            if not self.no_inscrito(self.usuario, nrc):
                Universidad.dicc_personas[self.usuario].botar_ramo(Curso.dicc_nrc[nrc])
                Universidad.dicc_personas[self.usuario].creditos -= Curso.dicc_nrc[nrc].creditos
                for apuestas in Pacmatico.dicc_ramos.values():
                    for i in range(len(apuestas)):
                        if apuestas[i].usuario == self.usuario:
                            if apuestas[i].nrc == nrc:
                                self.cont -= 1
                                aux = apuestas[i].extra
                                self.puntos += apuestas[i].extra
                                cred = Curso.dicc_nrc[nrc].creditos
                                Universidad.dicc_personas[self.usuario].botar_ramo(Curso.dicc_nrc[nrc])
                                Universidad.dicc_personas[self.usuario].creditos_apostados -= cred
                                apuestas.pop(i)
                for apuestas in Pacmatico.dicc_ramos.values():
                    for i in range(len(apuestas)):
                        if apuestas[i].usuario == self.usuario:
                            if apuestas[i].nrc != nrc:
                                if self.cont > 0:
                                    apuestas[i].resta += aux/self.cont

                print("Se borro el ramo satisfactoriamente")
            else:
                print("No se habia inscrito")

    def agregar_apuesta(self):
        nrc = input("Ingrese codigo nrc a cambiar apuesta: ")
        apuesta = float(input("Ingrese apuesta (te quedan {} puntos): ".format(self.puntos)))
        if self.puntos > apuesta:
            if Universidad.dicc_personas[self.usuario].creditos_apostados + Curso.dicc_nrc[nrc].creditos <=45:
                for apuestas in Pacmatico.dicc_ramos.values():
                    for i in range(len(apuestas)):
                        if apuestas[i].usuario == self.usuario:
                            if apuestas[i].nrc == nrc:
                                cred = Curso.dicc_nrc[nrc].creditos
                                Universidad.dicc_personas[self.usuario].creditos_apostados += cred
                                apuestas[i].extra += apuesta
                                self.puntos -= apuesta
                            else:
                                if self.cont > 1:
                                    apuestas[i].resta -= apuesta/(self.cont-1)
                for apuestas in Pacmatico.dicc_ramos.values():
                    for i in range(len(apuestas)):
                        if apuestas[i].puntos < 0:
                            Universidad.dicc_personas[self.usuario].creditos_apostados -= \
                            Curso.dicc_nrc[nrc].creditos
                            self.volver_atras()
                            print("Te quedaron ramos con menos de 0")
                            return
        self.actualizar()
        print("Cambio realizado... ")

    def volver_atras(self):
        for apuestas in Pacmatico.dicc_ramos.values():
            for i in range(len(apuestas)):
                apuestas[i].extra = apuestas[i].extra_antiguos
                apuestas[i].resta = apuestas[i].resta_antiguos
            self.puntos = self.puntos_antiguo

    def actualizar(self):
        for apuestas in Pacmatico.dicc_ramos.values():
            for i in range(len(apuestas)):
                apuestas[i].extra_antiguos = apuestas[i].extra
                print(apuestas[i].extra)
                apuestas[i].resta_antiguos = apuestas[i].resta
                print(apuestas[i].resta)
            self.puntos_antiguo = self.puntos

    def resultados(self):
        for apuestas in Pacmatico.dicc_ramos:
            Pacmatico.dicc_ramos[apuestas] = sorted(Pacmatico.dicc_ramos[apuestas], key=lambda x: x.puntos, reverse=True)
            Pacmatico.dicc_ramos[apuestas] = Pacmatico.dicc_ramos[apuestas][:Curso.dicc_nrc[apuestas].capacidad]
        for apuestas in Pacmatico.dicc_ramos.values():
            for i in range(len(apuestas)):
                if apuestas[i].usuario == self.usuario:
                    print("Ramo obtenido: {}".format(apuestas[i].nrc))


class Apuesta():

    def __init__(self, usuario, nrc, puntos):
        self.usuario = usuario
        self.nrc = nrc
        self.base = float(puntos)
        self.resta = 0
        self.resta_antiguo = 0
        self.extra = 0
        self.extra_antiguo = 0

    @property
    def puntos(self):
        return self.base + self.extra + self.resta

    def __str__(self):
        return str(self.nrc) + "\t" + str(self.puntos)


class Permisos(Sistema):

    def __init__(self, profesor):
        self.profesor = profesor

    def acceso(self, nrc):
        if Universidad.dicc_personas[self.profesor].nombre in Curso.dicc_nrc[nrc].profesor:
            print("Acceso concedido... ")
            return True
        else:
            print("Acceso denegado... ")
            return False

    def agregar_permiso(self, usuario, nrc):
        if usuario in Universidad.dicc_personas:
            if Universidad.dicc_personas[usuario].alumno:
                if self.existe_ramo(nrc):
                    if self.acceso(nrc):
                        if Universidad.dicc_personas[self.profesor].dar_permiso(usuario, nrc):
                            print("Se agrego correctamente el permiso... ")
                        else:
                            print("Ya tenia permiso... ")
            else:
                print("Es un profesor... no se pudo dar permiso")
        else:
            print("No existe ese usuario")

    def quitar_permiso(self, usuario, nrc):
        if usuario in Universidad.dicc_personas:
            if Universidad.dicc_personas[usuario].alumno:
                if self.existe_ramo(nrc):
                    if self.acceso(nrc):
                        if Universidad.dicc_personas[self.profesor].quitar_permiso(usuario, nrc):
                            print("Se quito correctamente el permiso... ")
                            return True
                        else:
                            print("No tenia permiso... ")
            else:
                print("Es un profesor... no se pudo quitar permiso")
        else:
            print("No existe ese usuario")
        return False
