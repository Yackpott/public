# coding=utf-8

import socket
import threading
import sys
import os
import time

global t
t = 10

# inicia servidor y probado en mac


class Cliente:

    def __init__(self):
        self.turno = False
        self.anterior = ""
        self.host = '127.0.0.1'
        self.port = 3500
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

    def bien(self, mensaje):
        historia = mensaje.split(" ")
        comparador = self.anterior.split(" ")
        if self.anterior == "" and len(historia) == 3:
            return True
        if len(historia) - 3 != len(comparador):
            return False
        try:
            for i in range(len(comparador)):
                if comparador[i] != historia[i]:
                    return False
        except IndexError:
            return False
        return True

    def recibir_mensajes(self):
        while True:
            data = self.s_cliente.recv(1024)
            mensaje = data.decode('utf-8')
            self.turno = True
            print(mensaje)
            if self.bien(mensaje):
                self.anterior = mensaje
                global t
                time.sleep(t)
            else:
                print("Ganaste")
                self.s_cliente.close()
                sys.exit()
                break
            os.system("clear")
            if mensaje == "exit":
                self.s_cliente.close()
                exit(0)

    def enviar(self, mensaje):
        if self.turno:
            if self.bien(mensaje):
                self.anterior = mensaje
                self.s_cliente.send(mensaje.encode('utf-8'))
            else:
                self.s_cliente.send(mensaje.encode('utf-8'))
                print("Perdiste")
                self.s_cliente.close()
                exit(0)
            if mensaje == "exit":
                self.s_cliente.close()
                exit(0)
            self.turno = False


class Servidor:

    def __init__(self):
        self.turno = True
        self.anterior = ""
        self.host = '127.0.0.1'
        self.port = 3500
        self.s_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Debemos hacer el setup para poder escuchar a los clientes que se
        # quieran conectar
        self.s_servidor.bind((self.host, self.port))
        # En este caso solo queremos escuchar un cliente
        self.s_servidor.listen(1)
        self.cliente = None
        self.aceptar()

    def bien(self, mensaje):
        historia = mensaje.split(" ")
        comparador = self.anterior.split(" ")
        if self.anterior == "" and len(historia) == 3:
            return True
        if len(historia) - 3 != len(comparador):
            return False
        try:
            for i in range(len(comparador)):
                if comparador[i] != historia[i]:
                    return False
        except IndexError:
            return False
        return True

    def recibir_mensajes(self):
        while True:
            data = self.cliente.recv(1024)
            mensaje = data.decode('utf-8')
            self.turno = True
            print(mensaje)
            if self.bien(mensaje):
                self.anterior = mensaje
                global t
                time.sleep(t)
            else:
                print("Ganaste")
                self.s_servidor.close()
                sys.exit()
                break
            os.system("clear")
            if mensaje == "exit":
                self.s_servidor.close()
                exit(0)

    def aceptar(self):
        cliente_nuevo, address = self.s_servidor.accept()
        self.cliente = cliente_nuevo
        thread_cliente = threading.Thread(
            target=self.recibir_mensajes, args=())
        thread_cliente.daemon = True
        thread_cliente.start()

    def enviar(self, mensaje):
        if self.turno:
            if self.bien(mensaje):
                self.anterior = mensaje
                self.cliente.send(mensaje.encode('utf-8'))
            else:
                self.cliente.send(mensaje.encode('utf-8'))
                print("Perdiste")
                self.s_servidor.close()
                exit(0)
            if mensaje == "exit":
                self.s_servidor.close()
                exit(0)
            self.turno = False


if __name__ == "__main__":

    pick = input("Ingrese S si quiere ser servidor o C si desea ser cliente: ")
    if pick == "S":
        server = Servidor()
        while True:
            texto = input()
            server.enviar(texto)

    elif pick == "C":
        client = Cliente()
        while True:
            texto = input()
            client.enviar(texto)
