Tarea01
===================


Nombre:  **Rodolfo Blanco**
Nro Alumno:  **14208369**

Se intentara en el presente archivo explicar el funcionamiento de la tarea 1.
Nota: se uso el pep8 de pycharm con 120 char.
Nota2: tome este ramo como electivo, revisen con amor por favor.

----------


Main.py
-------------

El main esta diseñado para correr la interfaz y usar las clases de sistema las cuales contienen Bummer y Pacmatico, además carga los archivos.

La funcion leer le use como un input modificado para poder salir con exit facilmente desde cualquier menu.

La funcion log in es para logearse ve los diccionarios si coinciden.

Luego se llaman las funcione Lector* que leer los archivos y los parsean.

Después puedo acceder a buscacursos o seguir por la rama de menús hacia Bummer y Pacmatico.

El sistema de input esta hecho para poder usar exit en casi cualquier parte y para poder volver atras en el menu.

Si se entra como Profesor, puedo quitar o agregar la tupla nrc alumno a una lista que después se usara para calcular si paso los requisitos.


----------


Sistema.py (Bummer)
-------------

Se inicia pidiendo si se quiere cargar el archivo con las bacanosidades o si se quiere calcular denuevo.

El calculo se realiza mediante el uso de matrices, se agregar en la matriz mat[i][j] el valor 1/(cuanta gente la persona i considera bkn) si considera bkn a la persona j, toma el valor 0 en otro caso.

Luego con numpy se eleva la matriz al cuadrado 50 veces (hasta que los valores paren de cambiar), y esos valor después los ordeno de mayor a menor y le asigno su persona correspondiente y ese es la bacanosidad de cada uno, ahí se divide el total por 10 grupo.

Agregar ramo comprueba si es la hora del grupo del usuario (que se pidió anteriormente), ve si existe el ramo, si no esta inscrito, si cumple con los requisitos.

Los requisitos los hice separando los paréntesis con recursión y para los correquisitos los puse con un c para compararlos y extendí la lista comparar con los ramos equivalentes.

Después comprueba que hayan vacantes, que no hayan ningún tipo de tope (evaluación, campus, cat-lab).

Se agrega el ramo y se hacen los cambios correspondientes, el botar ramo hace algo similar pero al revés.

Imprimir horario, guardar horario, y guardar evaluaciones se aprovechan de __str__() y __repr__() de horario y evaluaciones para hacerlo más fácil.

----------

Sistema.py (Pacmatico)
-------------

Guardo las apuestas en un diccionario que contiene listas por ramo.
Ver apuestas lo recorre y lo imprime.
Agregar ramo ve la condiciones y lo agrega.
Borrar ramo algo similar, la única de cambiar las apuestas es borrando el ramo.
Agregar apuesta cambia la apuesta y cambia las variables de puntaje.
Están las variables actualizar y volver atrás por el caso que se llegue a ramos con menos de 0 puntos.
Resultados me entrega los resultados mediante sorted, el valor más grande maximiza el puntaje efectivo, eso si no se explicaba que hacer con los correquisitos, si botarle ambos ramos o solo uno o esperar a las segunda vuelta o solex así que omití ese hecho ya que nunca habia tomado ramos con correquisitos con pucmatico y no se que hacer, es el unico supuesto usado en toda la tarea.

Apuesta se usa para el sorted y guardar datos y Permisos para accionar los permisos que dan los Profesores.

----------


Universidad.py
-------------

Lo más importante de este archivo es el diccionario que me guarda por usuario a todos los usuarios.
Ademas de que ahí se dan los permisos desde la clase profesores, se guardan en una lista en la forma de la tupla ya mencionada.

Curso.py
-------------

Se guardan los cursos en dos diccionarios, uno para siglas para conectar los dos archivos (uno no tiene nrc), y el otro de nrc para uso frecuente.

Cada horario es solo una hora y se guardan los datos en su propia clase.

Cada evaluacion es solo una por instancia de la clase.

__str__() y __repr__() se usa para imprimir bummer y buscacurso.

Funcionalidad.py
-------------

Parsea los archivos con un lambda que deja las lineas bonitas, tambien uso un while para el caso de cosas como los profesores que vienen en listas.

Hay subclases que hacen lo mismo pero con algunas excepciones y guardan los datos con el uso de **kwargs.