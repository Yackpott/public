from collections import deque
from PyQt4 import QtCore
import hashlib
import pickle
import os
import socket
import time
import threading

"""
Probado en mac osx el capitan
"""

HOST = "127.0.0.1"
PORT = 50000
RUTA = "descargas"


class Request:

    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class Event:

    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class Cliente(QtCore.QObject):
    lock = threading.Lock()
    trigger_login = QtCore.pyqtSignal(Event)
    trigger_carpetas = QtCore.pyqtSignal(Event)
    trigger_chat = QtCore.pyqtSignal(Event)

    def __init__(self, HOST, PORT, RUTA):
        super().__init__()
        self.host = HOST
        self.port = PORT
        self.ruta = RUTA
        self.widget_login = None
        self.widget_ventana = None
        self.cola = deque()
        self.observados = None
        self.conexion = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        thread_1 = threading.Thread(target=self.escuchar, args=())
        thread_1.daemon = True
        thread_1.start()
        thread_2 = threading.Thread(target=self.enviar, args=())
        thread_2.daemon = True
        thread_2.start()

    @staticmethod
    def agregar_largo(pick):
        return (len(pick)).to_bytes(4, byteorder='big') + pick

    @staticmethod
    def obtener_largo(byte):
        return int.from_bytes(byte, byteorder='big')

    @staticmethod
    def hashear(archivo):
        hash = hashlib.sha256()
        with open(archivo, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash.update(chunk)
        return hash.hexdigest()

    @staticmethod
    def recv(socket, largo):
        buff = bytes()
        for i in range(1024, largo, 1024):
            buff += socket.recv(1024)
        falta = largo - len(buff)
        buff += socket.recv(falta)
        return buff

    def escuchar(self):
        while self.conexion:
            info = self.socket.recv(4)
            largo = self.obtener_largo(info)
            pick = self.recv(self.socket, largo)
            dicc = pickle.loads(pick)
            if dicc["tipo"] == "pedir":
                self.pedir(dicc)
            elif dicc["tipo"] == "descargar":
                self.descargar(dicc)
            elif dicc["tipo"] == "info":
                self.info(dicc)
            elif dicc["tipo"] == "carpetas":
                self.trigger_carpetas.connect(
                    self.widget_ventana.carpetas_event)
                self.trigger_carpetas.emit(Event(dicc=dicc))
            elif dicc["tipo"] == "chat":
                self.trigger_chat.connect(self.widget_ventana.chat)
                self.trigger_chat.emit(Event(dicc=dicc))
            elif dicc["tipo"] == "login" or dicc["tipo"] == "nuevo":
                self.trigger_login.connect(self.widget_login.login_event)
                self.trigger_login.emit(Event(dicc=dicc))
            if "status" in dicc:
                print(dicc)

    def enviar(self):
        while self.conexion:
            time.sleep(1)
            if len(self.cola) > 0:
                byte = self.cola.popleft()
                self.socket.send(byte)

    def dumpear(self, req):
        pick = pickle.dumps(req)
        byte = self.agregar_largo(pick)
        self.cola.append(byte)

    def nuevo(self, user, password):
        req = Request(tipo="nuevo", user=user, password=password)
        self.dumpear(req)

    def login(self, user, password):
        dbp = "drobpox.dbp"
        if os.path.exists(dbp):
            with open(dbp, "r") as file:
                ob = [linea.strip() for linea in file.readlines()]
        else:
            ob = []
        req = Request(
            tipo="login", observados=ob, user=user, password=password)
        self.dumpear(req)

    def encontrar(self, path, carpeta, dicc):
        lista = os.listdir(path)
        for ruta in lista:
            dirr = path + "/" + ruta
            corta = carpeta + "/" + ruta
            try:
                if os.path.isfile(dirr):
                    dicc[self.hashear(dirr)] = corta
                elif os.path.isdir(dirr):
                    self.encontrar(dirr, corta, dicc)
            except Exception as err:
                print(err)

    # cada vez que  se apreta algun boton
    def carpetas(self):
        req = Request(tipo="carpetas")
        self.dumpear(req)

    def actualizar(self):
        dbp = "drobpox.dbp"
        if os.path.exists(dbp):
            dicc = dict()
            with open(dbp, "r") as file:
                self.observados = [linea.strip() for linea in file.readlines()]
            for path in self.observados:
                carpeta = path.split("/")[-1]
                self.encontrar(path, carpeta, dicc)
            req = Request(tipo="actualizar", dicc=dicc)
            self.dumpear(req)
        else:
            print("[Error]: no drobpox.dbp")

    def not_watching(self, carpeta):
        if os.path.exists("drobpox.dbp"):
            with open("drobpox.dbp", "r") as file:
                carpetas = [linea.strip() for linea in file.readlines()]
            if carpeta in carpetas:
                print("[Error]: already watching")
                return False
        return True

    def observar(self, carpeta):
        with self.lock:
            if self.not_watching(carpeta):
                with open("drobpox.dbp", "a+") as file:
                    if os.path.isdir(carpeta):
                        file.write(carpeta + "\n")
                    else:
                        print("[Error]: is not a dir")

    def pedir(self, dicc):
        ruta = dicc["archivo"]
        aux = ruta.split("/")[0]
        ruta = ruta[ruta.find("/") + 1:]
        for ant in self.observados:
            if aux in ant:
                ruta = ant + "/" + ruta
                break
        with open(ruta, "rb") as file:
            req = Request(tipo="subir", name=dicc["archivo"], file=file.read())
            self.dumpear(req)

    def historial(self, ruta):
        req = Request(tipo="historial", ruta=ruta)
        self.dumpear(req)

    def info(self, dicc):
        print(dicc["info"])

    def agregar(self, archivo):
        with open(archivo, "rb") as file:
            archivo = archivo.split("/")[-1]
            req = Request(tipo="agregar", name=archivo, file=file.read())
            self.dumpear(req)

    def descargar(self, dicc):
        name = self.ruta + "/" + dicc["name"]
        file = dicc["file"]
        carpetas = os.path.split(name)[0]
        if not os.path.exists(carpetas):
            os.makedirs(carpetas)
        with open(name, "wb+") as archivo:
            archivo.write(file)

    def download(self, archivo):
        if archivo.count(".") > 0:
            self.descargar_archivo(archivo)
        else:
            self.descargar_carpeta(archivo)

    def descargar_archivo(self, archivo):
        req = Request(tipo="descargar_archivo", name=archivo)
        self.dumpear(req)

    def descargar_carpeta(self, carpeta):
        req = Request(tipo="descargar_carpeta", carpeta=carpeta)
        self.dumpear(req)

    def eliminar(self, ruta):
        if ruta.find(".") == -1:
            lineas = ""
            with open("drobpox.dbp", "r") as file:
                linea = file.readline()
                while linea != "":
                    if ruta != linea.split("/")[-1].strip():
                        lineas += linea
                    linea = file.readline()
            with open("drobpox.dbp", "w+") as file:
                file.write(lineas)
        req = Request(tipo="eliminar", ruta=ruta)
        self.dumpear(req)

    """
    supuesto que si es carpeta no quiero agregarla a observada
    ya que no esta en el pc con ese nombre
    y se caeria al tratar de "observarla"
    ademas renombrar es lo mismo que mover
    """

    def renombrar(self, desde, hasta):
        req = Request(tipo="renombrar", desde=desde, hasta=hasta)
        self.dumpear(req)

    def conectar(self, usuario, otro):
        req = Request(tipo="conectar", usuario=usuario, otro=otro)
        self.dumpear(req)

    def chat(self, usuario, otro, texto):
        req = Request(tipo="chat", usuario=usuario, otro=otro, texto=texto)
        self.dumpear(req)

    def close(self):
        req = Request(tipo="desconexion")
        self.dumpear(req)
        while len(self.cola) > 0:
            time.sleep(0.5)
        self.socket.close()


if __name__ == "__main__":
    try:
        cliente = Cliente(HOST, PORT)
        cliente.observar("/users/rodolfo/desktop/Micro 1")
        cliente.observar("/users/rodolfo/desktop/Antropologia")
        cliente.nuevo("rfblanco", "hola123")
        cliente.login("rfblanco", "hola123")
        cliente.agregar("/users/rodolfo/desktop/test_hash.py")
        cliente.descargar_archivo("sebra.jnlp")
        cliente.actualizar()
        time.sleep(10)
        cliente.historial("Micro 1/Lecture+7.pdf")
        cliente.historial("Antropologia")
        time.sleep(5)
        cliente.historial("Progra")

    except Exception as err:
        print(err)

    else:
        while True:
            inp = input()
            if inp == "exit":
                break
    finally:
        cliente.close()
