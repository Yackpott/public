from PyQt4 import QtGui
from cliente import Cliente
from login import Login
from ventana import Ventana
import socket

HOST = "127.0.0.1"
PORT = 50000
RUTA = "descargas"

"""
intentar con
rfblanco: hola123
user: admin
"""

if __name__ == '__main__':
    try:
        app = QtGui.QApplication([])
        cliente = Cliente(HOST, PORT, RUTA)
        login = Login()
        ventana = Ventana()
        login.ventana = ventana
        login.cliente = cliente
        ventana.cliente = cliente
        cliente.widget_login = login
        cliente.widget_ventana = ventana
        app.exec_()
    except socket.error as err:
        print(err)
    finally:
        cliente.close()
