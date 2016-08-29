import socket
import threading
from gato import Gato, sys


class Service:

    def __init__(self, gato):
        self.gato = gato
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.puerto = 51028
        self.turno = None
        self.receptor = None

    def escuchar(self):
        while True:
            data = self.receptor.recv(1024)
            posicion = data.decode('ascii')
            posicion = posicion.split(",")
            if self.gato.revisar_ganador():
                exit(0)
            self.gato.editar_posicion(posicion)
            print(self.gato)

    def enviar(self, mensaje):
        if mensaje != "":
            self.receptor.send(mensaje.encode('ascii'))
            posicion = mensaje.split(",")
            if self.gato.revisar_ganador():
                exit(0)
            self.gato.editar_posicion(posicion)
            print(self.gato)


class Cliente(Service):

    def __init__(self, gato):
        super().__init__(gato)
        self.turno = "O"
        try:
            self.s.connect((self.host, self.puerto))
            self.receptor = self.s
        except socket.error:
            print("No fue posible realizar la conexión")
            sys.exit()


class Servidor(Service):

    def __init__(self, gato):
        super().__init__(gato)
        self.turno = "X"
        self.s.bind((self.host, self.puerto))
        self.s.listen(1)

    def aceptar(self):
        cliente, address = self.s.accept()
        self.receptor = cliente
        thread_cliente = threading.Thread(target=self.escuchar, args=())
        thread_cliente.daemon = True
        thread_cliente.start()


if __name__ == "__main__":
    gato = Gato()
    pick = input("Ingrese X si quiere ser servidor o O si desea ser cliente: ")
    if pick == "X":
        server = Servidor(gato)
        server.aceptar()
        while True:
            mensaje = input(
                "Jugador {0} debe ingresar la posicion en que desea jugar: ".format(server.gato.turno))
            server.enviar(mensaje)

    elif pick == "O":
        client = Cliente(gato)
        escuchador = threading.Thread(target=client.escuchar)
        escuchador.daemon = True
        escuchador.start()
        while True:
            mensajes = input(
                "Jugador {0} debe ingresar la posicion en que desea jugar: ".format(client.gato.turno))
            client.enviar(mensajes)
