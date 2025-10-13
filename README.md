# Repositorio - Tópicos de Inteligencia Artificial

Este repositorio está dedicado al curso de \_Tópicos de Inteligencia Artificial. En él se irán agregando documentos, investigaciones y materiales relacionados con las unidades del curso.

## Informacion

- **Universidad**: Instituto Tecnologico de México, Campus Culiacán
- **Materia** : Topicos de Inteligencia Artificial
- **Docente**: Dr. Zuriel Dathan Mora Félix

## Colaboradores

- Ramirez Medina Cristian Andrea
- Castro Figueroa Daniel Sebastian

## Unidades

# Unidad 1

**Descripción**: En esta unidad se encuentra un proyecto de investigación de inteligencia artificial e impacto ambiental

- [Proyecto de Investigación](Unidad1/Proyecto_de_Investigacion.pdf)

# Unidad 2

[Recocido Simulado — Sistema de enrutamiento para tiendas](./Unidad2/)

Este proyecto implementa una versión de recocido simulado para mejorar rutas de reparto entre Centros de Distribución y tiendas. Parte de una asignación inicial basada en distancia euclidiana, genera una solución inicial y aplica recocido simulado para reducir el costo total (distancia) de las rutas.

Estructura principal

- `main.py`: flujo principal. Carga datos, mapea coordenadas, genera solución inicial, ejecuta recocido simulado y guarda/visualiza resultados.
- `calcular_matriz_distancia.py`: genera la matriz de distancias (Haversine) a partir del fichero de puntos (`data/datos_distribucion_tiendas.xlsx`) y la guarda en `data/`.
- `src/soluciones.py`: funciones del algoritmo (generación de vecino, recocido simulado, cálculo de coste y utilidades).
- `src/cargar_data.py`: carga los datos (CDs y tiendas) y la matriz de distancias.
- `src/visualizacion.py`: funciones para generar mapas interactivos (Folium) de coordenadas, asignaciones y la solución final.
- `data/` y `output/`: carpetas para datos de entrada y resultados.

Requisitos

Se recomienda usar Python 3.12.0+ y los paquetes listados en `requirements.txt`.

Instalación rápida (PowerShell)

## Instalar dependencias

python -m pip install -r requirements.txt

Ejemplo de uso

1. Calcular la matriz de distancias (solo necesario la primera vez):

```powershell
python calcular_matriz_distancia.py
```

Esto leerá `data/datos_distribucion_tiendas.xlsx` y generará `data/matriz_distancias_haversine.xlsx`.

2. Ejecutar el flujo principal (genera mapas y resultados):

```powershell
python main.py
```

Salida esperada

- Archivos HTML con mapas en `output/`:
  - `1_mapa_inicial_coordenadas.html` — visualiza CDs y tiendas.
  - `2_mapa_asignaciones.html` — asignación inicial de tiendas a CDs.
  - `3_mapa_solucion_inicial.html` — recorrido de la solución inicial.
  - `4_mapa_mejor_solucion.html` — mapa de la mejor solución encontrada.
- Mensajes en consola con estadísticas del costo de la solución inicial y costo de la mejor solución.

### Ejemplo de mapas generados

|                           Mapa inicial | Asignaciones                           |
| -------------------------------------: | :------------------------------------- |
| ![Mapa inicial](/readme_img/Mapa1.png) | ![Asignaciones](/readme_img/Mapa2.png) |

|                           Solución inicial | Mejor solución                           |
| -----------------------------------------: | :--------------------------------------- |
| ![Solución inicial](/readme_img/Mapa3.png) | ![Mejor solución](/readme_img/Mapa4.png) |

Consejos y notas

- Ajustar parámetros del recocido en `main.py` (`temperatura_inicial`, `enfriamiento`, `iteraciones_por_temperatura`, `iteraciones_sin_mejora`) según tiempo disponible y calidad deseada.
- Si los mapas no se abren automáticamente, buscar los HTML generados en la carpeta `output/` para abrirlos en el navegador.
