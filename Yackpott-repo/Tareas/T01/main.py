from funcionalidad import LectorCursos, LectorEvaluaciones, LectorPersonas, LectorRequisitos
from sistema import Bummer, Pacmatico, Permisos
from universidad import Universidad
from curso import Curso

dir_cur = "cursos.txt"
dir_eval = "evaluaciones.txt"
dir_req = "requisitos.txt"
dir_per = "personas.txt"


def leer(mensaje):
    linea = input(mensaje)
    if linea == "exit":
        exit(0)
    else:
        return linea


def log_in(usuario, clave):
    try:
        if usuario != "" and clave != "" and usuario in Universidad.dicc_personas[usuario].usuario and clave in Universidad.dicc_personas[usuario].clave:
            return True
    except:
        pass
    return False

print("Cargando archivos...")
LectorCursos(dir_cur)
LectorEvaluaciones(dir_eval)
LectorRequisitos(dir_req)
LectorPersonas(dir_per)

texto_1 = """Ingrese modo:
        1 --> para ingresar al sistema
        2 --> para ver buscacursos
        exit --> en cualquier momento para salir \n"""
texto_2 = """Ingrese el sistema que quiere:
        1 --> BummerUC
        2 --> Pacmatico \n"""
texto_3 = """Ingrese opcion:
        1 --> para darle permiso alguien
        2 --> para quitarle permiso alguien
        atras --> para ir atras \n"""

linea = leer(texto_1)
while linea != "1" and linea != "2":
    print("Intente nuevamente...")
    linea = leer(texto_1)
if linea == "1":
    linea = leer(texto_2)
    while linea != "1" and linea != "2":
        print("Intente nuevamente...")
        linea = leer(texto_2)
    sistema = linea
    while True:
        usuario = leer("Ingrese usuario: ")
        clave = leer("Ingrese clave: ")
        while not log_in(usuario, clave):
            print("Usuario/Clave incorrectos... intente nuevamente")
            usuario = leer("Ingrese usuario: ")
            clave = leer("Ingrese clave: ")
        if Universidad.dicc_personas[usuario].alumno:
            if sistema == "1":
                bummer = Bummer(usuario)
            elif sistema == "2":
                pacmatico = Pacmatico(usuario)
        else:
            while True:
                linea = leer(texto_3)
                while linea != "1" and linea != "2" and linea != "atras":
                    print("Intente nuevamente...")
                    linea = leer(texto_3)
                if linea == "atras":
                    break
                permiso = Permisos(usuario)
                if linea == "1":
                    nrc = leer("Ingrese el nrc del ramo a dar permiso: ")
                    if nrc == "atras":
                        continue
                    alumno = leer("Ingrese el usuario del alumno: ")
                    if alumno == "atras":
                        continue
                    permiso.agregar_permiso(alumno, nrc)
                elif linea == "2":
                    nrc = leer("Ingrese el nrc del ramo a quitar permiso: ")
                    if nrc == "atras":
                        continue
                    alumno = leer("Ingrese el usuario del alumno: ")
                    if alumno == "atras":
                        continue
                    if permiso.quitar_permiso(alumno, nrc):
                        for ramo in Universidad.dicc_personas[alumno].lista_ramos:
                            if ramo.nrc == nrc:
                                Universidad.dicc_personas[alumno].botar_ramo(Curso.dicc_nrc[nrc])
                                Universidad.dicc_personas[alumno].creditos -= Curso.dicc_nrc[nrc].creditos
                                Curso.dicc_nrc[nrc].eliminar_alumno(Universidad.dicc_personas[alumno])
                                Curso.dicc_nrc[nrc].vacantes += 1
                                print("Se boto el ramo")
                            else:
                                print("Como no se habia tomado, no se boto el ramo")
elif linea == "2":
    while True:
        nrc = leer("Ingrese el codigo NRC del ramo a ver: ")
        if nrc == "exit":
            exit(0)
        print(Curso.dicc_nrc[nrc])
