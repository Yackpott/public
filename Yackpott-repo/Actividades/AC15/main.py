import threading
from time import sleep

alock = threading.Lock()
block = threading.Lock()


class Worker(threading.Thread):
    mean_data = dict()      # para guardar los promedios
    # Sientete libre para usar otras
    # variables estaticas aqui si quieres

    # programa el __init__
    # recuerda imprimir cual es el comando
    # para el cual se creo el worker
    def __init__(self, star_name, function_name):
        super().__init__()
        self.estrella = star_name
        self.func = function_name
        self.daemon = True

    @staticmethod
    def functions(func_name):
        """
        Este metodo recibe el nombre de una funcion
        y retorna una funcion que calcula promedio
        o varianza segun el argumento.
        Se necesita haber calculado promedio
        para poder calcular varianza
        """

        def mean(star_name):
            with open("{}.txt".format(star_name), 'r') as file:
                lines = file.readlines()
                ans = sum(map(lambda l: float(l), lines))/len(lines)
                Worker.mean_data[star_name] = ans
                return ans

        def var(star_name):
            prom = Worker.mean_data[star_name]
            with open("{}.txt".format(star_name), 'r') as file:
                lines = file.readlines()
                n = len(lines)
                suma = sum(map(lambda l: (float(l) - prom)**2, lines))
                return suma/(n-1)

        return locals()[func_name]

    # escriba el metodo run
    def run(self):
        if self.func == "var":
            try:
                Worker.mean_data[self.estrella]
                print(self.functions(self.func)(self.estrella))
            except:
                print("No se tiene aun el mean")
        elif self.func == "mean":
            print(self.functions(self.func)(self.estrella))

if __name__ == "__main__":
    lista = []
    command = input("Ingrese siguiente comando:\n")

    while command != "exit":
        estrella = command[command.find(" ")+1:]
        func = command[:command.find(" ")]

        def correr(estrella, func, lista):
            while True:
                aux = True
                for thread in lista:
                    if thread.func == func and thread.isAlive():
                        print("Esperando el otro thread")
                        aux = False
                if aux:
                    worker = Worker(estrella, func)
                    lista.append(worker)
                    worker.start()
                    break
                sleep(0.1)

        t1 = threading.Thread(target=correr, args=(estrella, func, lista))
        t1.start()
        command = input("Ingrese siguiente comando:\n")

    for thread in lista:
        if thread.isAlive():
            print(thread.func, "no termino de ejecutarse")
        else:
            print(thread.func, "termino de ejecutarse")

    # imprimir cuales comandos
    # alcanzaron a terminar, y cuales no
