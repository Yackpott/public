class Audifono:

    def __init__(self, frecuencia, impedancia, intensidad, **kwargs):
        super().__init__(**kwargs)
        self.frecuencia = frecuencia
        self.impedancia = impedancia
        self.intensidad = intensidad

    def escuchar(self, cancion):
        print('La cancion ' + str(cancion) +
              ' esta siendo reproducida desde un audifono')


class Frecuencia:

    def __init__(self, maximo, minimo):
        self.maximo = maximo
        self.minimo = minimo


class Circumaurales(Audifono):

    def __init__(self, aislacion, **kwargs):
        super().__init__(**kwargs)
        self.aislacion = aislacion


class Intraurales(Audifono):

    def __init__(self, incomodidad, **kwargs):
        super().__init__(**kwargs)
        self.incomodidad = incomodidad


class Inalambrico(Audifono):

    def __init__(self, rango, conectado=False, **kwargs):
        super().__init__(**kwargs)
        self.rango = rango
        self.conectado = conectado

    def escuchar(self, cancion):
        super().escuchar(cancion)
        print('La cancion ' + str(cancion) +
              ' esta siendo reproducida desde un audifono inalambrico')

    def conectarse(self, dist_reproductor):
        if dist_reproductor <= self.rango:
            self.conectado = True
            print('Se conecto exitosamente')
        else:
            print(
                'ERROR: Fuera de Rango')


class Bluetooth(Inalambrico):
    identificador = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Bluetooth.identificador += 1
        self.identificador = Bluetooth.identificador

    def escuchar(self, cancion):
        super().escuchar(cancion)
        print('La cancion ' + str(cancion) +
              ' esta siendo reproducida desde un audifono con Bluetooth')

if __name__ == '__main__':
    # Creamos instancia de bluetooth
    b1 = Bluetooth(
        rango=10, frecuencia=Frecuencia(10, 5), impedancia=5, intensidad=5)
    b1.conectarse(9)
    b1.conectarse(11)
    b1.escuchar('MOVES LIKE JAGGER')
    # Creamos instancia de inalambrico
    # Corremos sus metodos
    i1 = Inalambrico(
        rango=10, frecuencia=Frecuencia(10, 5), impedancia=3, intensidad=6)
    i1.conectarse(9)
    i1.conectarse(11)
    i1.escuchar('MOVES NOT LIKE JAGGER')
    # Creamos instancia de intraurales
    # Corremos sus metodos
    in1 = Intraurales(
        incomodidad=9, frecuencia=Frecuencia(10, 5),
        impedancia=3, intensidad=6)
    in1.escuchar('HAKUNA MATATA')
    # Creamos instancia circumaurales
    # Corremos los metodos
    c1 = Circumaurales(
        aislacion=5, frecuencia=Frecuencia(10, 5), impedancia=3, intensidad=6)
    c1.escuchar('LOS POLLITOS DICEN')
    # Creamos instancia de audifonos
    # Corremos sus metodos
    au1 = Audifono(frecuencia=Frecuencia(10, 5), impedancia=3, intensidad=6)
    au1.escuchar('NECESITAMOS UN 7')
