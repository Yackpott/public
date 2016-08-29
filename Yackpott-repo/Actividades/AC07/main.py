from functools import reduce
from itertools import groupby
from utils.parser import ApacheLogsParser


class BigAnalizador:

    def __init__(self, logs):
        self.logs = logs

    def bytes_transferidos(self):
        func1 = lambda x, y: x + y
        func2 = lambda x: x.size
        print(reduce(func1, map(func2, self.logs)))

    def errores_servidor(self):
        func1 = lambda x, y: x + y
        func2 = lambda x: 1 if x.status == 404 or x.status == 500 or x.status == 501 else 0
        print(reduce(func1, map(func2, self.logs)))

    def solicitudes_exitosas(self):
        func1 = lambda x, y: x + y
        func2 = lambda x: 1 if x.status == 200 or x.status == 302 or x.status == 304 else 0
        print(reduce(func1, map(func2, self.logs)))

    def url_mas_solicitada(self):
        self.logs = sorted(self.logs, key=lambda x: x.request)
        func = lambda x: x.request
        a = groupby(self.logs, key=lambda x: x.request)
        print(sorted(a, key=lambda x: x[1], reverse=True)[0])


if __name__ == '__main__':
    parser = ApacheLogsParser("./utils/nasa_logs_week.txt")
    logs = parser.get_apache_logs()
    biganalizador = BigAnalizador(logs)

    biganalizador.bytes_transferidos()
    biganalizador.errores_servidor()
    biganalizador.solicitudes_exitosas()
    biganalizador.url_mas_solicitada()
