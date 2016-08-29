import threading
import datetime


class Worker(threading.Thread):
    instances = list()
    mean_data = dict()
    dicc = dict()
    lock = threading.Lock()
    lock_2 = threading.Lock()

    def __init__(self, star_name, function_name):
        super().__init__()
        self.star_name = star_name
        self.func = function_name
        self.function = Worker.functions(function_name)
        self.command = "{} {}".format(function_name, star_name)
        print("Creando Worker para: {}".format(self.command))
        self.setDaemon(True)
        Worker.instances.append(self)

    @staticmethod
    def functions(func_name):
        """
        Este metodo estatico recibe el nombre de una funcion
        y retorna una FUNCION. Esta recibira un string
        con el nombre de la estrella, ya sea para
            - Cargarla al diccionario loaded_stars (open)
            - Calcular promedio (mean)
            - Calcular varianza (var)
        """

        def open(star_name):
            try:
                Worker.dicc[star_name]
            except:
                with Worker.lock:
                    f = __builtins__.open(star_name+".txt")
                    Worker.dicc[star_name] = f.readlines()
                    f.close()
            finally:
                return Worker.dicc[star_name]
            # completa aqui: debe leer el archivo
            # y cargarlo a un diccionario
            # TIP: desde el scope de esta funcion open,
            # puedes acceder al builtin "open" como
            # __builtins__.open

        def mean(star_name):
            # Modifica esto para que
            # no se abra el archivo nuevamente
            # sino que se trabaje con el diccionario
            # de estrellas ya cargadas
            try:
                Worker.dicc[star_name]
                lines = open(star_name)
                ans = sum(map(lambda l: float(l), lines))/len(lines)
                Worker.mean_data[star_name] = ans
                return ans
            except:
                print("[ERROR] No se ha cargado la estrella")
                return None

        def var(star_name):
            try:
                Worker.dicc[star_name]
                prom = Worker.mean_data[star_name]
                # modifica esto para que
                # no se abra el archivo nuevamente
                # sino que se trabaje con el diccionario
                # de estrellas ya cargadas
                lines = open("{}.txt".format(star_name))
                n = len(lines)
                suma = sum(map(lambda l: (float(l) - prom)**2, lines))
                return suma/(n-1)
            except:
                print("[ERROR] No se ha cargado la estrella")
                return None

        return locals()[func_name]

    def run(self):
        output = self.function(self.star_name)

        # Modifica aqui para que no se imprima
        # sino que se agregue la tupla a la lista de outputs
        if self.func != "open":
            if output != None:
                global output_list
                with Worker.lock_2:
                    output_list.append((self.getName(), self.command, output, datetime.datetime.now()))
                print("Termino")


if __name__ == "__main__":
    global output_list
    output_list = list()    # variables agregadas
    loaded_stars = dict()   # para esta actividad
    command = input("Ingrese siguiente comando:\n")

    while command != "exit":
        # Preocupate del comando "status"

        try:
            function, starname = command.split(" ")

            executed = False
            for w in Worker.instances:
                if w.command == command and w.isAlive():
                    print("[DENIED] Ya hay un worker ejecutando el comando")
                    executed = True
                    break

            if not executed:
                # preocupate de que solo se cree un worker
                # si la estrella ya fue cargada
                # al diccionario
                if function == "var" and starname not in Worker.mean_data:
                    print("[DENIED] No se puede calcular varianza "
                          "sin haber calculado el promedio antes!")

                elif starname in ["AlphaCentauri", "Arcturus",
                                  "Canopus", "Sirius", "Vega"]:
                    Worker(starname, function).start()

                else:
                    print("[DENIED] Comando invalido\n\t"
                          "El nombre de la estrella no es correcto")

        except (ValueError, KeyError) as err:
            print("[DENIED] {}\n\tComando invalido".format(type(err).__name__))

        command = input("Ingrese siguiente comando:\n")

    # Reemplazar esto por imprimir lista de outputs
    # y luego, imprimir los que aun no han terminado
    for out in output_list:
        print(out)
    print("Comandos ingresados por el usuario:")
    for w in Worker.instances:
        string = "NO alcanzo a terminar: " if w.isAlive()\
            else "Alcanzo a terminar: "
        print(string + w.command)
