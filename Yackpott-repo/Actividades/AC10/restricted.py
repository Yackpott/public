
class RestrictedAccess(type):

    def __new__(meta, nombre, base_clases, diccionario):
        meta.lista = diccionario["attributes"]
        diccionario["__init__"] = meta.f
        return super().__new__(meta, nombre, base_clases, diccionario)

    def f(self, *args, **kwargs):
        def get_x(self):
            x = self._x
            return x

        def set_x(self, val):
            raise AttributeError

        for i in range(len(args)):
            aux = str(getattr(RestrictedAccess, "lista")[i])
            setattr(self, aux, property(get_x,set_x))
            setattr(self, aux, args[i])

if __name__ == '__main__':
    class Person(metaclass=RestrictedAccess):
        attributes = ["name", "lastname", "alias"]
    p = Person("Bruce", "Wayne", "Batman")
    print(p.name, p.lastname, "es", p.alias, "!")
    # Bruce Wayne es Batman !
    p.alias = "Robin"
    # AttributeError: cant set attribute
