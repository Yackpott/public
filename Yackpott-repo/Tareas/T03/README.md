Tarea03
===================


Nombre:  **Rodolfo Blanco**

Nro Alumno:  **14208369**

Se intentara en el presente archivo explicar el funcionamiento de la tarea 3.
Nota: se uso el pep8 de pycharm con 120 char.

Comentarios antes de ver las secciones por archivos, la estructura general del programa esta dividida en vehículos de distintos tipos que poseen ataques, todos con sus respectivos métodos y atributos.
El juego es manipulado por la clase Sistema que hace casi toda la interacción con el usuario y las distintas clases.

El juego considera que el que lo juegue es un usuario avanzado experto en creación de sistemas para tomar ramos y experto en hackear redes, por eso juega con matrices que parten en el 0,0 y se mueve con vectores.

NOTA: lo hice con que cada vehiculo puede o atacar o moverse por turno, osea si hay n vehiculos puedo atacar hasta n veces.

No tuve tiempo para hacer la función computador, preferí un README mejor, que tratar de abarcar todo mal, el resto del juego funciona a la perfección.

No hay testing, tenía otra tarea para el mismo día, pero esta todo probado igual.
Es mejor tener el juego que no tenerlo pero tener funciones testeadas no unidas.

:(

Piedad porfavor...

----------


Main
-------------

Se debería pedir un input si es computador o oponente pero ya que como no funciona el computador, lo deje fijo en oponente.

Se crea mapa, rada, estadísticas, luego se rellena el mapa a través de las funciones del main que llaman a la clase mapa a medida que el usuario se lo va pidiendo.

El programa solo pide el punto más arriba y más a la izquierda y solo calcula a través del área hacia donde quedan las otras posiciones.

Luego se corren los turnos del sistema que es la parte básica del programa, se terminara la ejecución con un exit(0) desde sistema después de imprimir todas las estadisticas.

----------


Mapa
-------------

Matriz de nxn en donde cada punto es o un 0 o un objeto vehículo, tiene dos funciones, agregar y eliminar.

Agregar se usar cuando se esta creando el mapa y eliminar se usara desde sistema para cuando el daño es mayor a la resistencia y lo saca del mapa.

Todo lo hace simplemente recorriendo el mapa con fors y ver donde agregar o eliminar vehículos. 

----------

Estadísticas
-------------

En esta parte lo que se hace es ir agregando los barcos a medida que van muriendo y al final se agregan todos, después se analizan sus datos guardado es cada vehículo como atributo.

Nota:
BGM si pega 3 veces cuenta como 3 exitosos y 1 intento.
Daño por barco, no entendi que era, lo hice daño recibido por barco.
Con movimientos se refiere a unicos, no al largo del vector.
Más eficiente se refiere a exitos/intentos.


----------


Ataques
-------------

Se guardan los atributos y tiene un sistema a través de properties para saber si esta disponible un ataque, lo cual lo usara sistema para saber si tirar un error o seguir con el ataque.

Vehículos Marítimos y Aéreos
-------------

Guardan los ataques por vehículo y también están los datos de las resistencias, daño, etc.

Sistema
-------------

Acá se realiza el 90% del programa, se ve duro pero no lo es tanto, solo que tiene muchas excepciones ya que hay muchos casos posibles.

leer() sirve para poder salir en cada momento

turno() es la función principal ve si es jugador o computador y ve si hay vehículos con fuego del turno anterior para bajarles vida.

jugador() pide inputs de vehículos y luego de ataques y realiza estos ataques si están disponibles, si no, lanza un error.

recuperar() sirve para recuperar la vida con el puerto

atacar() realiza la baja de puntaje y no disponibilidad del ataque en el futuro ademas de ver los casos "especiales"

mover() pide un vector y si no hay nada realiza el movimiento y si es de un puesto a menos que sea la lancha, tira error si es un "vehículo" que no se puede mover

eliminar() elimina de la lista y mapa al vehículo

gano() es cuando ya se acabo el juego, imprime estadísticas y termina el programa

siguiente() es para que todos se enteren que paso un turno
