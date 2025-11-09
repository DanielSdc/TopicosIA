import random
import AG
import traceback

# Estado de tests
_estado = { 'completos': 0, 'fallidos': 0 }


def completo(name):
    """Marcar prueba como correcta e imprimir mensaje."""
    _estado['completos'] += 1
    print(f"Correcto: {name}")


def fallido(name, err=None):
    """Marcar prueba como fallida, imprimir mensaje y detalle opcional."""
    _estado['fallidos'] += 1
    print(f"Incorrecto: {name}")
    if err:
        print("Detalle:")
        print(err)


# Crear municipios primero (como pediste: fácil de leer)
m1 = AG.municipio(0, 0, "A")
m2 = AG.municipio(3, 4, "B")
m3 = AG.municipio(6, 8, "C")
lista = [m1, m2, m3]

# Prueba unitaria que verifica la distancia entre dos municipios sea correcta
def prueba_municipio_distancia():
    name = 'prueba_municipio_distancia'
    try:
        d = m1.distancia(m2)
        if abs(d - 5.0) < 1e-7:
            completo(name)
        else:
            fallido(name, f"Esperado 5.0, obtenido {d}")
    except Exception:
        fallido(name, traceback.format_exc())

# Prueba unitaria que verifica la distancia y la aptitud de una ruta
def prueba_aptitud_distancia_y_rutaApta():
    name = 'prueba_aptitud_distancia_y_rutaApta'
    try:
        ruta = [m1, m2, m3]
        apt = AG.Aptitud(ruta)
        d12 = m1.distancia(m2)
        d23 = m2.distancia(m3)
        d31 = m3.distancia(m1)
        esperado = d12 + d23 + d31
        if abs(apt.distanciaRuta() - esperado) < 1e-7 and abs(apt.rutaApta() - 1.0/esperado) < 1e-12:
            completo(name)
        else:
            fallido(name, f"Distancia esperada {esperado}, aptitud esperada {1.0/esperado}")
    except Exception:
        fallido(name, traceback.format_exc())

# Prueba unitaria que verifica crearRuta y poblacionInicial, es decir, que contienen los mismos municipios
def prueba_crearRuta_y_poblacionInicial():
    name = 'prueba_crearRuta_y_poblacionInicial'
    try:
        random.seed(0)
        ruta = AG.crearRuta(lista)
        if len(ruta) != len(lista):
            fallido(name, f"Longitud distinta: esperado {len(lista)} got {len(ruta)}")
            return
        nombres_ruta = sorted([m.nombre for m in ruta])
        nombres_lista = sorted([m.nombre for m in lista])
        if nombres_ruta == nombres_lista:
            pob = AG.poblacionInicial(5, lista)
            if len(pob) == 5 and all(len(r) == len(lista) for r in pob):
                completo(name)
            else:
                fallido(name, "poblacionInicial no tiene la forma esperada")
        else:
            fallido(name, f"Elementos distintos: {nombres_ruta} vs {nombres_lista}")
    except Exception:
        fallido(name, traceback.format_exc())


# Prueba unitaria que verifica la clasificación de rutas, es decir, que se ordenan correctamente por su aptitud de mayor a menor
def prueba_clasificacionRutas():
    name = 'prueba_clasificacionRutas'
    try:
        r1 = [m1, m2, m3]
        r2 = [m1, m3, m2]
        ranked = AG.clasificacionRutas([r1, r2])
        if len(ranked) == 2 and ranked[0][1] >= ranked[1][1]:
            completo(name)
        else:
            fallido(name, f"Ranking inesperado: {ranked}")
    except Exception:
        fallido(name, traceback.format_exc())
# Prueba unitaria que verifica que la reproducción produce un hijo con los mismos municipios
def prueba_reproduccion_preserva_elementos():
    name = 'prueba_reproduccion_preserva_elementos'
    try:
        padre1 = [m1, m2, m3]
        padre2 = [m3, m1, m2]
        random.seed(1)
        hijo = AG.reproduccion(padre1, padre2)
        if len(hijo) != len(padre1):
            fallido(name, f"Longitud distinta: {len(hijo)} vs {len(padre1)}")
            return
        if sorted([x.nombre for x in hijo]) == sorted([x.nombre for x in padre1]):
            completo(name)
        else:
            fallido(name, f"Elementos distintos en hijo: {[x.nombre for x in hijo]}")
    except Exception:
        fallido(name, traceback.format_exc())

# Prueba unitaria que verifica que la mutación produce un individuo con los mismos municipios y solo permuta su orden
def prueba_mutacion_preserva_elementos():
    name = 'prueba_mutacion_preserva_elementos'
    try:
        indiv = [m1, m2, m3]
        random.seed(2)
        mutado = AG.mutacion(list(indiv), razonMutacion=1.0)
        if len(mutado) != len(indiv):
            fallido(name, "Longitud distinta tras mutacion")
            return
        if sorted([x.nombre for x in mutado]) == sorted([x.nombre for x in indiv]):
            completo(name)
        else:
            fallido(name, f"Elementos distintos tras mutacion: {[x.nombre for x in mutado]}")
    except Exception:
        fallido(name, traceback.format_exc())


# Llamadas directas a las pruebas (sin clases ni run_all)
prueba_municipio_distancia()
prueba_aptitud_distancia_y_rutaApta()
prueba_crearRuta_y_poblacionInicial()
prueba_clasificacionRutas()
prueba_reproduccion_preserva_elementos()
prueba_mutacion_preserva_elementos()

print('\nResumen:')
print(f'  Completos: {_estado["completos"]}')
print(f'  Fallidos: {_estado["fallidos"]}')
if _estado['fallidos'] > 0:
    exit(1)
else:
    exit(0)
