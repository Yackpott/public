from functools import reduce
from curso import Curso


class Universidad:
    dicc_personas = dict()


class Persona(Universidad):

    def __init__(self, nombre, usuario, clave, **kwargs):
        self.dicc_personas[usuario] = self
        self.nombre = nombre
        self.usuario = usuario
        self.clave = clave


class Profesor(Persona):
    lista_permisos = []

    def __init__(self, nombre, usuario, clave, **kwargs):
        super().__init__(nombre, usuario, clave, **kwargs)
        self.alumno = False

    def dar_permiso(self, alumno, nrc):
        if (alumno, nrc) in Profesor.lista_permisos:
            return False
        else:
            Profesor.lista_permisos.append((alumno, nrc))
            return True

    def quitar_permiso(self, alumno, nrc):
        for i in range(len(Profesor.lista_permisos)):
            if (alumno, nrc) == Profesor.lista_permisos[i]:
                Profesor.lista_permisos.pop(i)
                return True
        return False


class Alumno(Persona):

    def __init__(self, nombre, usuario,
                 clave, ramos_pre, idolos, **kwargs):
        super().__init__(nombre, usuario, clave, **kwargs)
        self.curso_aprobados = ramos_pre
        self.idolos = idolos
        self.alumno = True
        self.lista_ramos = []
        self.creditos = 0
        self.creditos_apostados = 0

    def agregar_bkn(self, bkn):
        self.bkn = bkn

    def agregar_grupo(self, grupo):
        self.grupo = int(grupo)

    def agregar_relativa(self, relativa):
        self.relativa = float(relativa)

    def agregar_ramo(self, curso):
        self.lista_ramos.append(curso)

    def botar_ramo(self, curso):
        try:
            self.lista_ramos.pop(self.lista_ramos.index(curso))
        except:
            pass

    @property
    def horario(self):
        horarios = {1: Hora("8:30", "10:30"),
                    2: Hora("9:30", "11:30"), 3: Hora("10:30", "12:30"),
                    4: Hora("11:30", "13:30"), 5: Hora("12:30", "14:30"),
                    6: Hora("13:30", "15:30"), 7: Hora("14:30", "16:30"),
                    8: Hora("15:30", "17:30"), 9: Hora("16:30", "18:30"),
                    10: Hora("17:30", "19:30")}
        return horarios[self.grupo] if horarios[self.grupo] else None

    @property
    def max_creditos(self):
        return 55 + (6 - self.grupo) * 2

    @property
    def creditos_aprobados(self):
        lista = []
        for ramo in self.curso_aprobados:
            try:
                aux = Curso.dicc_siglas[ramo][0].creditos
                lista.append(aux)
            except:
                lista.append(0)
        return sum(lista)

    @property
    def nro_ramos(self):
        return len(self.lista_ramos)

    def __repr__(self):
        return self.nombre


class Hora:

    def __init__(self, inicio, fin):
        self.inicio = inicio
        self.fin = fin
