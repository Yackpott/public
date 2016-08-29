def compone_func_saludar(nombre):
    aux = 2
    print(id(aux))
    print(aux)
    def get_mensage():
        print("Entrando a get_mensaje()...")
        aux = 3
        print(id(aux))
        print(aux)
        return "Saludos para tí "+ nombre + "!"
    print(id(aux))
    print(aux)
    return get_mensage#en esta llamada se entra en la ejecución de get_mensaje

saludar = compone_func_saludar("Ana")
print(saludar())