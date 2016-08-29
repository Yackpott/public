### Distribución de puntajes

Requerimientos (**R**):

* **(2.0 pts)** R1: Sonda 4D 
* **(2.0 pts)** R2: Traidores
* **(2.0 pts)** R3: Pizzas

**Además, se descontará (0.2) puntos si no sigue formato de entrega.**

### Obtenido por el alumno
| R1 | R2 | R3 | Descuento |
|:---|:---|:---|:----------|
| 1.4 | 1.0 | 0 | 0 |

| Nota |
|:-----|
| **3.4** |

### Comentarios

* En **R1** no pides el número de consultas (-0.2), declaras mal la variable tupla (-0.2) y no transformas en tupla el input del usuario (-0.2).
* En **R2** tenías que usar dos ``set`` y encontrar la intersección (-1). Los sets son ideales en estos casos en que te interesa el conjunto en sí y no manipular los componentes:
```python
    bufalos = set()
    rivales = set()
    # Rellenar...
    traidores = bufalos & rivales
    # O también
    traidores = bufalos.intersection(rivales)
```
* **R3** no funciona :(.
* Te complicaste mucho para hacer esta AC, no era necesario crear clases :(.
