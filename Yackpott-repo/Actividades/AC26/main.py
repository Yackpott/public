import socket
import threading
import sys
import os


class Cliente:

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3505
        self.connection = True
        self.s_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Un cliente se puede conectar solo a un servidor.
            # El cliente revisa que el servidor esté disponible
            self.s_cliente.connect((self.host, self.port))
            # Una vez que se establece la conexión, se pueden recibir mensajes
            recibidor = threading.Thread(target=self.recibir_mensajes, args=())
            recibidor.daemon = True
            recibidor.start()
        except socket.error:
            print("No fue posible realizar la conexión")
            sys.exit()

    def recibir_mensajes(self):
        mensaje = ""
        while True:
            data = self.s_cliente.recv(1024)
            if data is None:
                break
            mensaje += data
            print(mensaje)
            if mensaje[:4] == b"exit":
                self.terminar()
        mensaje = mensaje.split(b"***")
        for i in range(len(mensaje)-1):
            with open(mensaje[i].decode("utf-8"), "wb") as file:
                file.write(mensaje[i+1])

    def enviar(self, lista):
        if lista == "exit":
            self.s_cliente.send(lista.encode("utf-8", errors = 'ignore'))
        else:
            mensaje = bytearray(b"")
            for archivo in lista:
                (filepath, filename) = os.path.split(archivo)
                mensaje.extend(b"***")
                mensaje.extend(b"archivo")
                mensaje.extend(b"***")
                with open(archivo, "rb") as file:
                    mensaje.extend(file.read())
            self.s_cliente.send(mensaje)

    def terminar(self):
        self.connection = False
        self.s_cliente.close()
        exit(0)


class Servidor:

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3505
        self.connection = True
        self.s_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Debemos hacer el setup para poder escuchar a los clientes que se
        # quieran conectar
        self.s_servidor.bind((self.host, self.port))
        # En este caso solo queremos escuchar un cliente
        self.s_servidor.listen(1)
        self.cliente = None
        self.aceptar()

    def recibir_mensajes(self):
        mensaje = ""
        while True:
            data = self.s_servidor.recv(1024)
            if data is None:
                break
            mensaje += data
            print(mensaje)
            if mensaje[:4] == b"exit":
                self.terminar()
        mensaje = mensaje.split(b"***")
        for i in range(len(mensaje)-1):
            with open(mensaje[i].decode("utf-8"), "wb") as file:
                file.write(mensaje[i+1])

    def aceptar(self):
        cliente_nuevo, address = self.s_servidor.accept()
        self.cliente = cliente_nuevo
        thread_cliente = threading.Thread(
            target=self.recibir_mensajes, args=())
        thread_cliente.daemon = True
        thread_cliente.start()

    def enviar(self, lista):
        if lista == "exit":
            self.cliente.send(lista.encode("utf-8", errors = 'ignore'))
        else:
            mensaje = bytearray(b"")
            for archivo in lista:
                (filepath, filename) = os.path.split(archivo)
                mensaje.extend(b"***")
                mensaje.extend(b"archivo")
                mensaje.extend(b"***")
                with open(archivo, "rb") as file:
                    mensaje.extend(file.read())
            self.cliente.send(mensaje)

    def terminar(self):
        self.connection = False
        self.s_servidor.close()
        exit(0)


def mostrar(lista):
    print(lista)


def agregar(lista):
    archivos = os.listdir(os.curdir)
    for archivo in archivos:
        print(archivo)
    linea = input("Seleccione archivo a agregar: ")

    file = os.path.realpath(".") + "/" + linea
    print(file)
    if os.path.exists(file):
        lista.append(file)
    else:
        print("No es un archivo")


def quitar(lista):
    print(lista)
    linea = input("Seleccione archivo a eliminar: ")
    if linea in lista:
        lista.remove(linea)
    else:
        print("No es un archivo")


def enviar(lista, obj):
    print("Por enviar: ")
    print(lista)
    obj.enviar(lista)


def ruta():
    ruta = input("Ingrese la ruta de la carpeta: ")
    os.chdir(ruta)


def terminar(obj):
    obj.enviar("exit")
    obj.terminar()


if __name__ == "__main__":
    os.chdir("Archivos/")
    lista = []
    opciones = """
1 -- > Mostrar por enviar
2 -- > Agregar archivos
3 -- > Quitar archivos
4 -- > Enviar archivos
5 -- > Poner ruta
exit -- > Terminar comunicacion
"""
    pick = input("Ingrese S si quiere ser servidor o C si desea ser cliente: ")
    if pick == "S":
        server = Servidor()
        while True:
            texto = input(opciones)
            if texto == "1":
                mostrar(lista)
            elif texto == "2":
                agregar(lista)
            elif texto == "3":
                quitar(lista)
            elif texto == "4":
                enviar(lista, server)
            elif texto == "5":
                ruta()
            elif texto == "exit":
                terminar(server)

    elif pick == "C":
        client = Cliente()
        while True:
            texto = input(opciones)
            if texto == "1":
                mostrar(lista)
            elif texto == "2":
                agregar(lista)
            elif texto == "3":
                quitar(lista)
            elif texto == "4":
                enviar(lista, client)
            elif texto == "5":
                ruta()
            elif texto == "exit":
                terminar(client)
