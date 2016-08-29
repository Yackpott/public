# coding=utf-8

# Recuerda borrar los 'pass'. Pudes borrar si quieres los comentarios.


class Commit:
    id = 0

    def __init__(self, message, changes):
        #############
        # COMPLETAR:
        # 'changes' es una lista de tuplas.
        # Puedes modificar esta clase a gusto tuyo.
        #############
        self.message = message
        self.changes = changes
        self.id = Commit.id
        Commit.id += 1


class Branch:

    def __init__(self, nombre, padre):
        self.nombre = nombre
        self.padre = padre
        self.cola = None
        self.cabeza = None

    #############
    # COMPLETAR:
    # Crear __init__ con lo que consideres necesario
    #############

    def new_commit(self, commit):  # Agregar nodo
        if not self.cabeza:
            self.cabeza = commit
            self.cola = self.cabeza
        else:
            self.cola.siguiente = commit
            self.cola = self.cola.siguiente

    def pull(self, id):
        files = []
        nodo = self.cabeza
        while nodo is not None or nodo.valor.id - 1 == id:
            for accion, archivo in nodo.valor.changes:
                if accion in "DELETE":
                    if files.count(archivo) > 0:
                        files.remove(archivo)
                elif accion in "CREATE":
                    if files.count == 0:
                        files.append(archivo)
            nodo = nodo.siguiente
        return files


class Repository:

    def __init__(self, name, master=None, ):
        self.name = name
        self.master = self.create_branch('Master', None)
        self.lista_branch = []

        #############
        # COMPLETAR:
        # Crear branch 'master'.
        # Crear commit inicial y agregarlo a 'master'.
        #############

    def create_branch(self, new_branch_name, from_branch_name):

        if from_branch_name is None:
            self.lista_branch.append(Branch(new_branch_name, None))

        else:
            self.lista_branch.append(Branch(new_branch_name, from_branch_name))

    def branch(self, branch_name):
        for branch in self.hijos:
            if branch.nombre == branch_name:
                return branch
        #############
        # COMPLETAR:
        # Retornar la branch con el nombre 'branch_name'.
        #############

    def checkout(self, commit_id):
        for branch in self.hijos:
            for nodo in branch:
                if nodo.valor.id == commit_id:
                    return branch.pull(commit_id)

        #############
        # COMPLETAR:
        # Buscar el commit con cierta id y retornar el estado del repositorio
        # hasta ese commit. Puede estar en cualquier branch.
        #############


if __name__ == '__main__':
    # Ejemplo de uso
    # Puedes modificarlo para probar esto pero al momento de la corrección
    # el ayudante borrará cualquier cambio y restaurará las siguientes lineas
    # a su estado original (como se muestran aquí).

    repo = Repository("syllabus 2.0")

    repo.branch("master").new_commit(Commit(
        message="agregado readme",
        changes=[("CREATE", "README.md")]
    ))

    repo.branch("master").new_commit(Commit(
        message="archivos base",
        changes=[("CREATE", "main.py"), ("CREATE", "clases.py")]
    ))

    # Creamos una rama del estado actual de 'master'
    repo.create_branch("desarrollo-de-vistas", 'master')
    repo.branch("desarrollo-de-vistas").new_commit(Commit(
        message="imagenes",
        changes=[("CREATE", "main.jpg"), ("CREATE", "user.png")]
    ))

    repo.branch("desarrollo-de-vistas").new_commit(Commit(
        message="cambiar instrucciones",
        changes=[("DELETE", "README.md"), ("CREATE", "instrucciones.html")]
    ))

    repo.branch("master").new_commit(Commit(
        message="datos recolectados",
        changes=[("CREATE", "data.csv")]
    ))

    print(repo.branch("master").pull())
    # Esperamos que el repo esté así:
    # ['.jit', 'README.md', 'main.py', 'clases.py', 'data.csv']

    print(repo.branch("desarrollo-de-vistas").pull())
    # Esperamos que el repo esté así:
    # ['.jit', 'main.py', 'clases.py',
    #  'main.jpg', 'user.png', 'instrucciones.html']

    print(repo.checkout(4))
    # Esperamos que el repo esté así:
    # ['.jit', 'README.md', 'main.py', 'clases.py', 'main.jpg', 'user.png']

    print(repo.checkout(1))
    # Esperamos que el repo esté así:
    # ['.jit']
