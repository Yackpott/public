from servidor import Servidor

"""
Probado en mac osx el capitan
"""

HOST = "127.0.0.1"
PORT = 50000

RUTA = "host"

"""
intentar con
rfblanco: hola123
user: admin
"""

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
