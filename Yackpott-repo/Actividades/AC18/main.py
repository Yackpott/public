import random
import simpy

SIM_TIME = 500
INTERVAL = 10
TABLES = 3
NAME = "Cliente {0}"


def paciencia(cliente):
    return 2 * cliente.priority + 7


class Cliente():

    def __init__(self, *args, **kwargs):
        self.priority = kwargs['priority']
        self.name = kwargs['name']
        self.arrive = kwargs['arrive']
        self.number = kwargs['arrival_number']
        self.exit = None


class Restaurante():

    def __init__(self, env, capacity):
        self.env = env
        self.mesas = simpy.PriorityResource(env, capacity=capacity)
        self.__clientes = []
        self.n_atendidos = 1

    def espera(self, cliente):
        self.__clientes.append(cliente)
        with self.mesas.request(priority=cliente.priority) as req:
            results = yield req | self.env.timeout(paciencia(cliente))
            if req in results:
                print("El {} fue atendido en {} y lleva {}".format(
                    cliente.name, self.env.now, self.env.now - cliente.arrive))
                if 0.1 > random.random():
                    yield self.env.timeout(random.uniform(7, 12))
                    print("El {} se fue porque recibio el llamado en {} y estuvo {}".format(
                        cliente.name, self.env.now, self.env.now - cliente.arrive))
                else:
                    yield self.env.timeout(random.uniform(30, 40))
                    print("El {} se quedo hasta el final hasta {} y estuvo {}".format(
                        cliente.name, self.env.now, self.env.now - cliente.arrive))

            else:
                print("El {} se aburre y se fue en {} y estuvo {}".format(
                    cliente.name, self.env.now, self.env.now - cliente.arrive))


def generador_clientes(env, lambdat, res):
    count = 0
    while True:
        yield env.timeout(random.expovariate(1 / lambdat))
        priority = random.randint(0, 25)
        cliente = Cliente(name=NAME.format(
            count), priority=priority, arrive=int(env.now), arrival_number=count)
        print("{0} ha arrivado al restaurant al instante {1} y \
                es el cliente numero {2}  del dia".format
              (
                  cliente.name,
                  env.now,
                  count
              ))
        count += 1
        env.process(res.espera(cliente))


if __name__ == '__main__':
    env = simpy.Environment()
    res = Restaurante(env, TABLES)
    env.process(generador_clientes(env, INTERVAL, res))
    env.run(until=SIM_TIME)
