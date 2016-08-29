class Singleton(type):
    dicc = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in Singleton.dicc:
            Singleton.dicc[cls] = super().__call__(*args, **kwargs)
        return Singleton.dicc[cls]

if __name__ == '__main__':
    class A(metaclass=Singleton):

        def __init__(self, value):
            self.val = value
    a = A(10)  # Se crea una instancia de A
    # Se retorna la instancia que ya estaba creada print(a.val, b.val)
    b = A(20)
    # 10 10
    print(a is b)  # True
