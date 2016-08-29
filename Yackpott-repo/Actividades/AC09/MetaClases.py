class MetaRobot(type):

    def __new__(meta, nombre, base_clases, diccionario):
        if nombre != "Robot":
            raise NameError("No es robot")
        diccionario["creador"] = "Yackpott"
        diccionario["ip_inicio"] = "190.102.62.283"
        diccionario["check_creator"] = meta.check_creator
        diccionario["cortar_conexion"] = meta.cortar_conexion
        diccionario["cambiar_nodo"] = meta.cambiar_nodo
        return super().__new__(meta, nombre, base_clases, diccionario)

    def check_creator(self):
        for programador in self.creadores:
            if self.creador == programador:
                print("El creador se encuentra en la lista")
                return True
        print("El creador no se encuentra en la lista")
        return False

    def cortar_conexion(self):
        if not(self.Verificar()):
            self.actual.hacker = 0
            print("Se encontro un hacker y se corto la conexion")
        else:
            print("No se encontro un hacker")

    def cambiar_nodo(self, nodo):
        aux = self.actual.ide
        self.actual = nodo
        print("Nodo proveniento {}, Nodo destino {}".format(
            aux, self.actual.ide))
