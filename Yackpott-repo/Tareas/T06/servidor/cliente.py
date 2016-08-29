class Request:

    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class Cliente:

    def __init__(self, socket):
        self.socket = socket
        self.conexion = True
        self.credenciales = False
        self.usuario = None
        self.observados = None
