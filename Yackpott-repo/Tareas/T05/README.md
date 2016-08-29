Tarea05
===================


Nombre:  **Rodolfo Blanco**
Nro Alumno:  **14208369**

Se intentara en el presente archivo explicar el funcionamiento de la tarea 5.
Nota: se uso el pep8 de pycharm con 120 char.

Comentario 1: funciona todo, primera vez que termino una tarea :)
Comentario 2: parte del codigo fue sacada de la ayudantia 8.

----------


Main
-------------

Abre la ventana inicial.

----------


Inicial
-------------

La ventana de inicio, tiene un botón para iniciar.
Si es la segunda vez, ósea,  que se acabo ya una partida, muestra el puntaje final.

----------

Juego
-------------

Tiene la parte de la ventana del juego.
Tiene:
    Direccionar (jugador, zombies, balas)
    Mover (jugador, zombies, balas)
    Calcular movimiento
    No choque
    Puntaje
    Crear zombies y objetos (cerveza y pistolas)
    Pausa

Cosas importantes, se conecta con los objetos que son QThreads y QObject con eventos.
    

----------


Objetos
-------------

Tiene los threads de Balas, Jugador, Zombie y las clases de los eventos para poder manejarlos y así poder comunicarse con la ventana juego.

Las balas ven con si están cerca de un zombie, y si lo están lo matan.
El jugador ve que siga con vida y moverse con las WASD.
Los zombies ven si están cerca del jugador y lo dañan.
