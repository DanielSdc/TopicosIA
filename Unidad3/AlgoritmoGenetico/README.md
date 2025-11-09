# Algoritmo Genético - Rutas (TSP simple)

Este repositorio contiene una implementación de un algoritmo genético para optimizar rutas entre municipios (problema del viajante - TSP). El código está pensado para experimentar con operadores de cruce, mutación y selección.

Resumen

- `AG.py`: implementación del modelo (clase `municipio`, `Aptitud`, y funciones del algoritmo genético: creación de rutas, población, selección, reproducción, mutación y ejecución principal).
- `test_ag.py`: runner de pruebas manuales que ejecuta 6 comprobaciones básicas e imprime por prueba "Correcto" o "Incorrecto".

Estructura principal

- `AG.py` — código principal del algoritmo genético y utilidades.
- `test_ag.py` — pruebas sencillas y manuales. Llamar directamente con `python test_ag.py` para ver mensajes por prueba.

Requisitos

Se recomienda usar Python 3.12.0+ y los paquetes listados en `requirements.txt`.

Instalación rápida (PowerShell)

## Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

Ejecutar el algoritmo (script principal)

```powershell
python AG.py
```

Salida esperada.
`AG.py` imprimirá la distancia inicial y la final, y la mejor ruta encontrada. Nota: `AG.crearRuta` imprime las rutas internamente; si prefieres una salida más limpia, elimina el `print(route)` dentro de `AG.crearRuta`.

Ejecutar pruebas

Para ejecutar las pruebas manuales y ver un mensaje por cada test:

```powershell
python test_ag.py
```

Salida esperada

- `test_ag.py` imprimirá por cada prueba `Correcto: <nombre_prueba>` o `Incorrecto: <nombre_prueba>` y un resumen final.

Notas

- Para experimentar: cambia parámetros en la llamada a `algoritmoGenetico` (tamaño de población, probabilidad de mutación, número de generaciones) y observa la mejora en la distancia.
