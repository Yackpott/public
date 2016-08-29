# coding=utf-8

import requests
from collections import defaultdict
from argparse import ArgumentParser

# Debe tener los atributos:
# * _id (string)
# * name (string)
# * votes (diccionario string: int)


class Table:
    votos = defaultdict(int)
    listas = []

    def __init__(self, _id, name):
        self._id = _id
        self.name = name

    def actualizar(self, json):
        for k, v in json.items():
            self.votos[k] = self.votos[k] + v

    @classmethod
    def creador(cls, **kwargs):
        return cls(**kwargs)


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Votos elecciones FEUC 2015',
    )

    parser.add_argument(
        '-u',
        '--user',
        type=str,
        required=True,
        help="Ponga su Usuario",
    )

    parser.add_argument(
        '-p',
        '--password',
        type=str,
        required=True,
        help="Ponga su Clave",
    )

    args = parser.parse_args()

    user = args.user
    password = args.password

    auth = (user, password)

    lista_tables = []
    url = ('http://votaciometro.cloudapp.net/api/v1/tables')
    response = requests.get(url, auth=auth)
    for json in response.json():
        lista_tables.append(Table.creador(**json))

    url = ('http://votaciometro.cloudapp.net/api/v1/lists')
    response = requests.get(url, auth=auth)
    Table.listas = response.json()

    url = 'http://votaciometro.cloudapp.net/api/v1/tables/{}'

    for table in lista_tables:
        nueva = url.format(table._id)
        response = requests.get(nueva, auth=auth)
        table.actualizar(response.json()["votes"])

    aux = (None, 0)
    for k, v in Table.votos.items():
        print("Lista: {} --> {}".format(k, v))
        if v > aux[1]:
            aux = (k, v)
    print("El ganador es {}, con {} votos".format(aux[0], aux[1]))
