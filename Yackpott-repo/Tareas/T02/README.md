Tarea 2:
Rodolfo Blanco
14208369

Lista:
practicamente simulo casi todas las funciones de list

Main:
se usa 1m movimientos porque con mas no sacaba mas arcos unicos.

Grafo:
se basa en recorrer mediante random todo, haciendolo muchas veces, guardo los nodos unicos y los arcos unicos, por medio del algo in milista, por eso modifique el __eq__.
uso arboles binarios para buscar para que todo se haga mas rapido
guardo todo en el arbol y en una lista que se usaran en distintas partes

BFS:
el algoritmo que use fue agregar el arco a una lista y saco el ultimo y agrego al final de la lista los vecinos del nodo sacado.

Doble:
saco si el hijo del hijo es el padre, entonces lo agrego y con recursion y guardado en texto y listas agrego hasta el mas largo, sin agregar repetidos, no tiene sentido

Ciclos:
ver que el hijo del hijo del hijo sea el padre o el hijo del ultimo tambien lo sea, si agrego los repetidos ya q como no son conexiones dobles, pueden no ocurrir.

Flujo:
guardo la capacidad minimo de los que llevo, guardo todos los alcanzable o alguna vez alcanzables y voy siempre por el maximo con recursion veo todos los caso.

No Ciclo:
veo si hay un ciclo dentro de un ciclo, ya que tengo que mantener el fuertemente conexo, osea elimino si estoy en dos ciclos o no podria llegar a todos los nodos, si hay doble ciclo elimino un arco con recursion veo todos los casos.
