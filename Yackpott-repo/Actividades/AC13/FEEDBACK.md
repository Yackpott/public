### Distribución de puntajes

Requerimientos (**R**):

* **(2.0 pts)** R1: Crear el método setUP y tearDown
* **(0.5 pts)** R2: Test de revisar_nombre 
* **(0.5 pts)** R3: Test de revisar_formato
* **(1.0 pts)** R4: Test de revisar_verificador
* **(1.0 pts)** R5: Test de revisar_orden
* **(1.0 pts)** R6: Test de descontar
* **(1.0 pts)** R7: Test de get_palabras y get_descuento (0.5 cada uno)
* **(1.0 pts)** BONUS: Crear nuevo programa corrector sin errores

**Además, se descontará (0.2) puntos si no sigue formato de entrega.**

### Obtenido por el alumno
| R1 | R2 | R3 | R4 | R5 | R6 | R7 | BONUS | Descuento |
|:---|:---|:---|:---|:---|:---|:---|:------|:----------|
| 2.0 | 0.3| 0.5 | 1.0 | 1.0 | 0 | 0.9 | 0 | 0 |

**Para un 7.0 se necesitan 7 puntos**

| Nota |
|:-----|
| 5.89 |

### Comentarios

Debiera detectar las funciones con error (FAILED (failures=4))
get_descuento, 
get_palabras, 
revisar_formato y 
revisar_nombre

self.assertTrue(self.corr2.revisar_nombre()) es F
self.assertEquals(self.corr2.get_descuento(),0) es 0.5 de desc
Bien!

* Sin Comentarios
