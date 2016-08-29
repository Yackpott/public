class Emergencias:

    pass


class Cuartel(Emergencias):

    def __init__(self):
        self.tipo = self.__class__.__name__


class Comisaria(Emergencias):

    def __init__(self):
        self.tipo = self.__class__.__name__


class Hospital(Emergencias):

    def __init__(self):
        self.tipo = self.__class__.__name__
