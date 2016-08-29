Tarea 06
===================


Nombre:  **Rodolfo Blanco**
Nro Alumno:  **14208369**

Notas:

Hice el bonus del 15% del cliente op.

Lo que no hice:
las carpetas compartidas.
emoji: lo intente con todas las recomendaciones del foro y probe el mismo codigo que en otros SO funcionaba pero en el mio no funciono nunca asi que no lo hice, porfa no me bajen por eso, si me eche caleta de tiempo y no funciona nomas en mi SO.
mandar archivos por chat.

Hay dos cuentas:
rfblanco --> hola123
user --> admin

La cuenta rfblanco ademas ya viene con un par de carpetas y archivos para que las prueben.


----------


Login y Creación de cuentas
-------------

Las cuentas se crean como dicen las instrucciones, con el hash (sha256) + salta(64 bytes random A-Z, a-z, números), el cual se guarda en bd.dbp

Cada usuario ahi tiene su propia carpeta con su numero de usuario y ahi se guardan sus archivos e historial de archivos.


----------


Interfaz
-------------

La interfaz es bastante intuitiva, lo ínico importante de mencionar es que mover y renombrar los puse en el mismo botón, al final son lo mismo, ahí hay que poner la ruta y si cambias el nombre del archivo se renombra, ademas de moverse.

Descargar lo baja al cliente la carpeta o archivo y lo deja en descargas.

Historial lo imprime en la consola como dice el enunciado.

Actualizar ve las carpetas y las  sincroniza.


----------

Chat
-------------

Funciona asincrono, osea puedo mandar mensajes en vivo o con el otro usuario desconectado. 

Arriba pongo el nombre del usuario a conectar y carga altiro el historial del chat de la conversación.

El emoji no funciona por lo ya mencionado y mandar archivos tampoco.

----------

Extra
-------------

Hay que abrir servidor/main.py y cliente/main.py

Ademas comente harto código, sobretodo en las partes que encontraba mas subjetivas.