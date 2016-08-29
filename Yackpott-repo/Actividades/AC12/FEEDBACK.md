### Distribución de puntajes

Requerimientos (**R**):

* **(3.0 pts)** R1: Se manejan todos los errores que generan la falla del sistema
* **(3.0 pts)** R2: Se notifica qué no se pudo hacer y la razón del error

**Se descontará (1.5) puntos por cada error que no se maneje (0.75 por no manejo y 0.75 por no notificación del error).**

### Obtenido por el alumno
| R1 | R2 | R3 | R4 | R5 | R6 | Descuento |
|:---|:---|:---|:---|:---|:---|:----------|
| 2 | 3 | 0 | 0 | 0 | 0 | 0 |

| Nota |
|:-----|
| **6.0** |

### Comentarios

Bueno el manejo de los errores pero te falta imprimir el tipo de excepción capturada por ejemplo “KeyError”; intenta hacer algo como esto:

except Exception as err:
    print("[ERROR]", type(err).__name__)
saludos!