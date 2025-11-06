import os
import numpy as np
import pandas as pd
import pyswarms as ps
from plots import limpiar_frames, guardar_frame, guardar_frame_costo, plot_mejor_solucion, crear_gif_iteraciones
from funcion import calcular_costos_vectorizado

# Parámetros del Problema
# ===========================================================================================
cantidad_sensores = 10                # Número de sensores a ubicar
dimensiones = cantidad_sensores * 2  # Dimensiones = sensores * 2 (lat, lon)
numero_particulas = 20               # Partículas para búsqueda más robusta


# Cargar CSV con coordenadas de cultivos 
base = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base, "data", "cultivos.csv")

# Obtener limites dinamicos del mapa para ubicar sensores dentro de estos rangos
df = pd.read_csv(csv_path)
df["Latitud"] = pd.to_numeric(df["Latitud"], errors="coerce")
df["Longitud"] = pd.to_numeric(df["Longitud"], errors="coerce")
df = df.dropna(subset=["Latitud", "Longitud"]) 
if df.empty:
    raise ValueError("El CSV no contiene coordenadas válidas.")
lat_min, lat_max = df["Latitud"].min(), df["Latitud"].max()     # Obtener min/max latitud
lon_min, lon_max = df["Longitud"].min(), df["Longitud"].max()   # Obtener min/max longitud


# ===========================================================================================
# Pyswarms necesita los límites como dos arrays separados:
# Uno para todos los límites inferiores (Min)
# Otro para todos los límites superiores (Max)
# Agrupamos los límites en una tupla (formato necesario para PySwarms)

limite_inferior = [lat_min, lon_min] * cantidad_sensores
limite_superior = [lat_max, lon_max] * cantidad_sensores

limites = (np.array(limite_inferior), np.array(limite_superior))


# Parametros del Algoritmo
# ===========================================================================================
opciones = {'w': 0.9, 'c1': 2, 'c2': 2} # Parámetros del PSO que favorecen convergencia
                                        # w : inercia
                                        # c1 : atracción personal
                                        # c2 : atracción global
w_decay = 0.99                          # Decaimiento de la inercia por iteración (mejora la convergencia)
iters = 200                             # Ejecutar optimización con  (más iteraciones para favorecer convergencia)

                    
frame_every = 5                         # Para guardar frame cada N iteraciones

# Creación del Enjambre (Optimizador)
# ==========================================================================================
# Pasar los parámetros al constructor del optimizador
optimizador = ps.single.GlobalBestPSO(
    n_particles=numero_particulas,  # Número de partículas en el enjambre
    dimensions=dimensiones,         # Dimensiones del problema (lat, lon por cada sensor)
    options=opciones,               # Coeficientes del PSO
    bounds=limites,                 # Límites de búsqueda Max/Min (lat, lon)
)


# Imprimir resumen de configuración
print(f"¡Enjambre creado exitosamente con {numero_particulas} partículas!")
print(f"Dimensiones de cada partícula: {dimensiones}")
print(f"Límites (lat_min, lat_max): ({lat_min}, {lat_max})")
print(f"Límites (lon_min, lon_max): ({lon_min}, {lon_max})")
print(f"Objeto optimizador: {optimizador}")



# Preparar los datos de cultivos (Nx2 array)
datos_cultivos = df[["Latitud", "Longitud"]].to_numpy()
    
print(f"Ejecutando optimización de prueba ({iters} iteraciones)...")

frames_dir = os.path.join(base, "frames")
# Al iniciar el programa, eliminar frames de ejecuciones previas (frame_*.png)
# De esta forma los frames se conservan tras crear el GIF y sólo se borran
# cuando el usuario vuelva a ejecutar el programa, para evitar acumulación innecesaria.
limpiar_frames(frames_dir)
# Asegurar que el directorio existe para guardar los nuevos frames
os.makedirs(frames_dir, exist_ok=True)


# Metodo para llamar la función de costo desde PySwarms
# ===========================================================================================
# Recibe: X: array (P, D) con P partículas y D dimensiones
# Devuelve: costos: array (P,) con el costo para cada partícula
def objetivo_for_opt(X):
    return calcular_costos_vectorizado(X, datos_cultivos)

# Ejecutar optimización iterando manualmente una iteración a la vez
# (esto nos permite guardar el frame a partir de la mejor solución devuelta por cada iteración deseada)
saved_frames = []

# Historial del mejor costo por iteración (para el plot de evolución)
best_cost_history = []

global_best_cost = float("inf")  # Mejor costo global encontrado
global_best_pos = None           # Mejor posición global encontrada
TOL = 1e-9                       # Tolerancia para considerar mejora significativa
iteraciones_sin_mejora = 150                   # Iteraciones sin mejora para parada
last_improvement = 0             # Iteración de la última mejora
    
# Ciclo principal de optimización de N iteraciones    
for it in range(1, iters + 1):
        
    # Obtener mejor costo y posición tras una iteración
    # Pasamos la función objetivo y ejecutamos 1 iteración
    costo_iteracion, posision_iteracion = optimizador.optimize(objetivo_for_opt, iters=1, verbose=False)
      
    # Decaimiento del coeficiente de inercia 'w' para favorecer convergencia
    optimizador.options['w'] = float(optimizador.options.get('w', opciones['w']) * w_decay)
       


    # Actualizar el mejor global sólo si el costo mejora estrictamente (evitar reemplazos por empates)
    if costo_iteracion + TOL < global_best_cost:
        global_best_cost = float(costo_iteracion)
        global_best_pos = np.asarray(posision_iteracion).copy()
        last_improvement = it

    # Guardar mejor solución encontrada hasta ahora
    mejor_costo = global_best_cost
    mejor_pos = global_best_pos

    # Registrar el mejor costo actual en el historial (para plotting)
    best_cost_history.append(mejor_costo)

    # Guardar frame mostrando todas las partículas y la mejor posición
    guardar_frame(optimizador=optimizador, frames_dir=frames_dir, it=it, dimensiones=dimensiones,
                global_best_pos=global_best_pos, pos_it=posision_iteracion, costo_it=costo_iteracion, frame_every=frame_every,
                saved_frames=saved_frames, df=df)

    # (No guardar aquí el frame de costo por iteración: solo guardaremos
    # un único frame final después de la optimización.)

    # Verificar si se cumple criterio de parada por falta de mejora
    if (it - last_improvement) >= iteraciones_sin_mejora:
        print(f"No hubo mejora en {iteraciones_sin_mejora} iteraciones; deteniendo en iter {it}.")
        break


output_dir = os.path.join(base, "output")
print("Mejor costo encontrado:", mejor_costo)
print("Mejor posición (vector):", mejor_pos)

# Guardar la mejor solución en un archivo de texto
out_best_txt = os.path.join(output_dir, "best_solution.txt")
with open(out_best_txt, "w", encoding="utf-8") as f:
    f.write(f"mejor_costo: {mejor_costo}\n")
    f.write("mejor_pos:\n")
    f.write(",".join(map(str, mejor_pos)))

print(f"Mejor solución guardada en: {out_best_txt}")


# Generar un plot rápido con cultivos y sensores (mejor solución)
plot_mejor_solucion(df, mejor_pos, output_dir)

# Guardar un único frame final con la evolución del mejor costo
final_iter = len(best_cost_history)
saved_frames_cost = []
guardar_frame_costo(best_cost_history, output_dir, final_iter, 1, saved_frames_cost)

# Combinar frames generados durante la optimización en un GIF
crear_gif_iteraciones(frames_dir, output_dir)
