class Curso:
    dicc_nrc = dict()
    dicc_siglas = dict()

    def __init__(self, curso, sigla, sec, NRC, profesor,
                 campus, ofr, disp, cred,
                 apr, eng, retiro, **kwargs):
        Curso.dicc_nrc[NRC] = self
        if sigla in Curso.dicc_siglas.keys():
            Curso.dicc_siglas[sigla].append(self)
        else:
            Curso.dicc_siglas[sigla] = [self]
        self.nombre = curso
        self.sigla = sigla
        self.seccion = sec
        self.nrc = NRC
        self.profesor = profesor
        self.campus = campus
        self.capacidad = int(ofr)
        self.vacantes = int(disp)
        self.creditos = int(cred)
        self.aprobacion = apr
        self.ingles = eng
        self.retiro = retiro
        self.lista_alumnos = []
        self.horarios = []
        self.evaluaciones = []

    @property
    def ocupados(self):
        return self.capacidad - self.vacantes

    def agregar_horario(self, horario):
        self.horarios.append(horario)

    def agregar_evaluacion(self, evaluacion):
        self.evaluaciones.append(evaluacion)

    def agregar_requisitos(self, prerreq, equiv, **kwargs):
        self.requisitos = prerreq
        self.equivalencias = equiv

    def agregar_alumno(self, usuario):
        self.lista_alumnos.append(usuario)

    def eliminar_alumno(self, alumno):
        try:
            self.lista_alumnos.pop(self.lista_alumnos.index(alumno))
        except:
            print("El alumno no existe, no se pudo eliminar")

    def __str__(self):
        aux = """
        Nombre: {}
        Sigla: {}
        Seccion: {}
        NRC: {}
        Profesor(es): {}
        Campus: {}
        Capacidad: {}
        Vacantes: {}
        Ocupados: {}
        Creditos: {}
        Aprobacion: {}
        Ingles: {}
        Retiro: {}
        Alumnos: \n{}\n
        Horario:\n{}\n
        Evaluaciones: \n{}\n
        Requisitos: {}
        Equivalencias: {}
        """.format(self.nombre, self.sigla, self.seccion, self.nrc,
                   self.profesor, self.campus, self.capacidad, self.vacantes,
                   self.ocupados, self.creditos, self.aprobacion, self.ingles,
                   self.retiro, self.lista_alumnos, self.horarios,
                   self.evaluaciones, self.requisitos, self.equivalencias)
        return(aux)


class Horario:

    def __init__(self, tipo, dia, hora, sala, **kwargs):
        self.tipo = tipo
        self.dia = dia
        self.hora = hora
        self.sala = sala

    def __repr__(self):
        return "\n" + self.dia + str(self.hora) + "\t" + self.tipo + "\t sala:" + self.sala


class Evaluacion:

    def __init__(self, tipo, fecha, sigla, sec, **kwargs):
        self.tipo = tipo
        self.fecha = fecha
        self.sigla = sigla
        self.seccion = sec

    def __repr__(self):
        return "\n" + self.tipo +"\t" +self.fecha + "\t" + self.sigla + "-" + self.seccion
