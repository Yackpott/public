from datetime import datetime
from cliente import Cliente, Request
import hashlib
import pickle
import random
import os
import shutil
import socket
import string
import threading

"""
Probado en mac osx el capitan
"""

HOST = "127.0.0.1"
PORT = 50000

RUTA = "host"


class Servidor:
    lock = threading.Lock()
    chat_lock = threading.Lock()

    def __init__(self, HOST, PORT, RUTA):
        os.chdir(RUTA)
        self.host = HOST
        self.port = PORT
        self.clientes = []
        self.conexion = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        thread_1 = threading.Thread(target=self.aceptar, args=())
        thread_1.daemon = True
        thread_1.start()

    @staticmethod
    def agregar_largo(pick):
        return (len(pick)).to_bytes(4, byteorder='big') + pick

    @staticmethod
    def obtener_largo(byte):
        return int.from_bytes(byte, byteorder='big')

    @staticmethod
    def generate_salt():
        n = 64
        let = string.ascii_lowercase + string.ascii_uppercase + string.digits
        return ''.join(random.SystemRandom().choice(let)for _ in range(n))

    @staticmethod
    def hash(clave, salt):
        return hashlib.sha256((clave + salt).encode()).hexdigest()

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

    @property
    def fecha(self):
        return datetime.now().isoformat(" ").split(".")[0]

    def aceptar(self):
        while self.conexion:
            socket, addr = self.sock.accept()
            cliente = Cliente(socket)
            self.clientes.append(cliente)
            thread_2 = threading.Thread(target=self.escuchar, args=(cliente,))
            thread_2.daemon = True
            thread_2.start()

    def escuchar(self, cliente):
        opciones = {"carpetas": self.carpetas,
                    "actualizar": self.actualizar,
                    "subir": self.subir,
                    "historial": self.historial,
                    "agregar": self.agregar,
                    "descargar_archivo": self.descargar_archivo,
                    "descargar_carpeta": self.descargar_carpeta,
                    "eliminar": self.eliminar,
                    "renombrar": self.renombrar,
                    "conectar": self.conectar,
                    "chat": self.chat,
                    "desconexion": self.desconexion}
        while self.conexion and cliente.conexion:
            info = cliente.socket.recv(4)
            if len(info) > 0:
                largo = self.obtener_largo(info)
                pick = self.recv(cliente.socket, largo)
                req = pickle.loads(pick)
                print("Request:", req.tipo)
                if req.tipo == "nuevo":
                    self.nuevo(cliente, req)
                elif req.tipo == "login":
                    self.login(cliente, req)
                elif cliente.credenciales:
                    opciones[req.tipo](cliente, req)
                else:
                    cliente.conexion = False

    def enviar(self, cliente, dicc):
        pick = pickle.dumps(dicc)
        byte = self.agregar_largo(pick)
        cliente.socket.send(byte)

    def nuevo(self, cliente, req):
        if not os.path.exists("bd.dbp") \
                or (not self.verificador(req.user, req.password)
                    and not self.existe_usuario(req.user)):
            salt = self.generate_salt()
            user = req.user
            password = self.hash(req.password, salt)
            with self.lock:
                with open("bd.dbp", "a+") as bd:
                    bd.write(user + "\n" + salt + "\n" + password + "\n")
            dicc = {"tipo": "nuevo", "status": "ok"}
            os.makedirs(user)
        else:
            dicc = {"tipo": "nuevo", "status": "[Error]: already exists"}
        self.enviar(cliente, dicc)

    def verificador(self, user, password):
        with self.lock:
            with open("bd.dbp", "r") as bd:
                linea = bd.readline().strip()
                while linea != "":
                    if user == linea:
                        salt = bd.readline().strip()
                        cripto = bd.readline().strip()
                        if cripto == self.hash(password, salt):
                            return True
                        else:
                            break
                    linea = bd.readline().strip()
        return False

    def existe_usuario(self, user):
        with self.lock:
            with open("bd.dbp", "r") as bd:
                linea = bd.readline().strip()
                while linea != "":
                    if user == linea:
                        return True
                    linea = bd.readline().strip()
        return False

    def login(self, cliente, req):
        if self.verificador(req.user, req.password):
            cliente.credenciales = True
            cliente.usuario = req.user
            cliente.observados = req.observados
            dicc = {"tipo": "login", "status": "ok"}
        else:
            cliente.credenciales = False
            dicc = {"tipo": "login", "status": "[Error]: bad user/pass"}
        self.enviar(cliente, dicc)

    def encontrar(self, path, dicc):
        if not os.path.exists(path):
            os.makedirs(path)
        lista = os.listdir(path)
        for ruta in lista:
            dirr = path + "/" + ruta
            try:
                if os.path.isfile(dirr):
                    dicc[self.hashear(dirr)] = dirr[dirr.find("/") + 1:]
                elif os.path.isdir(dirr):
                    self.encontrar(dirr, dicc)
            except Exception as err:
                print(err)

    def carpetear(self, path, carpetas):
        lista = os.listdir(path)
        for ruta in lista:
            dirr = path + "/" + ruta
            try:
                if os.path.isfile(dirr):
                    aux = dirr.split("/")[-1]
                    carp = "/".join(path.split("/")[1:])
                    if carp not in carpetas:
                        carpetas[carp] = [aux]
                    else:
                        carpetas[carp].append(aux)
                elif os.path.isdir(dirr):
                    self.carpetear(dirr, carpetas)
            except Exception as err:
                print(err)

    def carpetas(self, cliente, req):
        carpetas = dict()
        self.carpetear(cliente.usuario, carpetas)
        dicc = {"tipo": "carpetas", "carpetas": carpetas}
        self.enviar(cliente, dicc)
        print("Mostrar Carpetas")

    def actualizar(self, cliente, req):
        dicc = req.dicc
        host_dicc = dict()
        lista = [linea.split("/")[-1] for linea in cliente.observados]
        for carpeta in lista:
            carpeta = cliente.usuario + "/" + carpeta
            self.encontrar(path=carpeta, dicc=host_dicc)
        lista = []
        for k, v in host_dicc.items():
            if k not in dicc:
                lista.append(k)
                self.remove(cliente, cliente.usuario + "/" + v)
        for k in lista:
            del host_dicc[k]
        for k, v in dicc.items():
            if k not in host_dicc:
                self.pedir(cliente, v)
            elif host_dicc[k] != v:
                desde = cliente.usuario + "/" + host_dicc[k]
                hasta = cliente.usuario + "/" + v
                self.rename(cliente, desde, hasta)

    def pedir(self, cliente, archivo):
        dicc = {"tipo": "pedir", "archivo": archivo}
        self.enviar(cliente, dicc)
        print("Se pidio", archivo)

    def registrar(self, cliente, archivo, evento):
        hist = cliente.usuario + "/historial.dbp"
        if not os.path.exists(hist):
            with open(cliente.usuario + "/historial.dbp", "wb+") as historial:
                pickle.dump(dict(), historial)
        with open(hist, "rb") as file:
            dicc = pickle.load(file)
        k = cliente.usuario + "/" + archivo
        if k in dicc:
            dicc[k].append(evento)
        else:
            dicc[k] = [evento]
        with open(hist, "wb") as file:
            pickle.dump(dicc, file)

    """
    historial no es recursivo, solo de la carpeta que se pide
    """

    def historial(self, cliente, req):
        output = []
        hist = cliente.usuario + "/" + "historial.dbp"
        if not os.path.exists(hist):
            with open(cliente.usuario + "/historial.dbp", "wb+") as historial:
                pickle.dump(dict(), historial)
        with open(hist, "rb") as file:
            dicc = pickle.load(file)
        path = cliente.usuario + "/" + req.ruta
        if os.path.isdir(path):
            lista = os.listdir(path)
            for ruta in lista:
                ruta = cliente.usuario + "/" + req.ruta + "/" + ruta
                try:
                    if os.path.isfile(ruta):
                        output.extend(dicc[ruta])
                except Exception as err:
                    print(err)
        try:
            output.extend(dicc[path])
        except Exception as err:
            print(err)
        self.info(cliente, output)

    def info(self, cliente, output):
        output = "\n".join(output)
        dicc = {"tipo": "info", "info": output}
        self.enviar(cliente, dicc)
        print(output)

    def add(self, cliente, archivo):
        evento = "{} - ADDED\t '{}' by {}".format(
            self.fecha, archivo, cliente.usuario)
        self.registrar(cliente, archivo, evento)
        print("Se adirio", archivo)

    def remove(self, cliente, archivo):
        os.remove(archivo)
        archivo = archivo[archivo.find("/") + 1:]
        evento = "{} - REMOVED\t '{}' by {}".format(
            self.fecha, archivo, cliente.usuario)
        self.registrar(cliente, archivo, evento)
        print("Se removio", archivo)

    def rename(self, cliente, desde, hasta):
        os.rename(desde, hasta)
        desde = desde[desde.find("/") + 1:]
        hasta = hasta[hasta.find("/") + 1:]
        evento = "{} - RENAMED\t '{}' to '{}' by {}".format(
            self.fecha, desde, hasta, cliente.usuario)
        self.registrar(cliente, hasta, evento)
        print("Se renombro", desde, hasta)

    def subir(self, cliente, req):
        archivo = cliente.usuario + "/" + req.name
        file = req.file
        ruta = os.path.split(archivo)[0]
        print(ruta)
        if not os.path.exists(ruta):
            os.makedirs(ruta)
        with open(archivo, "wb+") as nueva:
            nueva.write(file)
        self.add(cliente, req.name)

    def agregar(self, cliente, req):
        name = cliente.usuario + "/" + req.name
        archivo = req.file
        with open(name, "wb+") as file:
            file.write(archivo)
        self.add(cliente, req.name)

    def descargar(self, cliente, name):
        ruta = cliente.usuario + "/" + name
        with open(ruta, "rb") as file:
            dicc = {"tipo": "descargar", "name": name, "file": file.read()}
            self.enviar(cliente, dicc)
        print("Se descargo", name)

    def descargar_archivo(self, cliente, req):
        name = cliente.usuario + "/" + req.name
        if os.path.exists(name):
            self.descargar(cliente, req.name)
        else:
            dicc = {"tipo": "descargar", "status": "not {}".format(req.name)}
            self.enviar(cliente, dicc)

    def descarga_recursiva(self, cliente, path):
        lista = os.listdir(path)
        for ruta in lista:
            dirr = path + "/" + ruta
            try:
                if os.path.isfile(dirr):
                    dirr = dirr[dirr.find("/") + 1:]
                    self.descargar(cliente, dirr)
                elif os.path.isdir(dirr):
                    self.descarga_recursiva(cliente, dirr)
            except Exception as err:
                print(err)

    def descargar_carpeta(self, cliente, req):
        path = cliente.usuario + "/" + req.carpeta
        self.descarga_recursiva(cliente, path)

    """
    supuesto si elimino carpeta, se guarda en el historial de la carpeta
    """

    def eliminar(self, cliente, req):
        ruta = cliente.usuario + "/" + req.ruta
        if os.path.exists(ruta):
            try:
                if os.path.isfile(ruta):
                    self.remove(cliente, ruta)
                else:
                    shutil.rmtree(ruta)
                evento = "{} - REMOVED\t '{}' by {}".format(
                    self.fecha, req.ruta, cliente.usuario)
                self.registrar(cliente, req.ruta, evento)
                print("Se removio", req.ruta)
            except Exception as err:
                print(err)
    """
    supuesto si renombro carpeta, se guarda en el historial de la carpeta
    ademas renombrar es lo mismo que morverla
    """

    def renombrar(self, cliente, req):
        desde = cliente.usuario + "/" + req.desde
        hasta = cliente.usuario + "/" + req.hasta
        if os.path.exists(desde):
            try:
                shutil.move(desde, hasta)
                evento = "{} - RENAMED\t '{}' to '{}' by {}".format(
                    self.fecha, desde, hasta, cliente.usuario)
                self.registrar(cliente, req.hasta, evento)
                print("Se renombro", desde, hasta)
            except Exception as err:
                print(err)

    def conectar(self, cliente, req):
        otro = req.otro
        boleano = False
        usuario = cliente.usuario
        with self.lock:
            with open("bd.dbp", "r") as bd:
                linea = bd.readline().strip()
                while linea != "":
                    if otro == linea and usuario != linea:
                        boleano = True
                        break
                    linea = bd.readline().strip()
        if boleano:
            texto = self.chat_historial(cliente, req)
            texto = "".join(texto)
            dicc = {"tipo": "chat", "otro": otro, "status": "ok", "texto": texto}
            self.enviar(cliente, dicc)
        else:
            dicc = {"tipo": "otro", "status": "[Error]: not exists"}
            self.enviar(cliente, dicc)

    def ruta_chat(self, cliente, req):
        path = "Chat"
        if not os.path.exists(path):
            os.makedirs(path)
        op1 = path + "/" + req.usuario + "-" + req.otro
        op2 = path + "/" + req.otro + "-" + req.usuario
        if os.path.exists(op1):
            op = op1
        else:
            op = op2
        return op

    def chat_historial(self, cliente, req):
        op = self.ruta_chat(cliente, req)
        with self.lock:
            with open(op, "r") as file:
                return file.readlines()

    def chat(self, cliente, req):
        op = self.ruta_chat(cliente, req)
        with self.chat_lock:
            with open(op, "a+") as file:
                file.write("\n"+req.texto)
        self.enviar_chat(req.otro, req.texto)

    def enviar_chat(self, otro, texto):
        for cl in self.clientes:
            if cl.usuario == otro:
                dicc = {"tipo": "chat", "texto": texto}
                self.enviar(cl, dicc)

    def desconexion(self, cliente, req):
        cliente.conexion = False
        self.clientes.remove(cliente)

    def close(self):
        self.sock.close()


if __name__ == "__main__":
    try:
        servidor = Servidor(HOST, PORT, RUTA)
    except Exception as err:
        print(err)
    else:
        while True:
            inp = input()
            if inp == "exit":
                break
    finally:
        servidor.close()
