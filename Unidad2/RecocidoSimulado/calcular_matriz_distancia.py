import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from config import DATA_DIR, DATOS_PUNTOS, MATRIZ_DISTANCIAS

print("Iniciando")
#Directorio del archivo excel con las coordenadas
directorio_archivo = DATA_DIR + DATOS_PUNTOS

#Asegurarse de que el archivo existe y se puede leer
try:
    df = pd.read_excel(directorio_archivo)
except FileNotFoundError:
    print(f"Error: El archivo '{directorio_archivo}' no se encontró.")
    exit()

#Utilizar las columnas correctas para latitud y longitud
coordenadas = df[['Latitud_WGS84', 'Longitud_WGS84']].values

#Convertir las coordenadas de grados a radianes para la formula haversine
coordenadas_rad = np.radians(coordenadas)

#Radio de la Tierra en kilómetros
R = 6371

#Función para calcular la distancia haversine entre dos puntos
def haversine(u, v):
    lat1, lon1 = u
    lat2, lon2 = v
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

matriz_distancia = squareform(pdist(coordenadas_rad, haversine))

dist_matrix_df = pd.DataFrame(matriz_distancia, index=df['Nombre'], columns=df['Nombre'])

# Guardar la matriz en un nuevo archivo CSV
output_file = DATA_DIR + MATRIZ_DISTANCIAS
dist_matrix_df.to_excel(output_file)

print("\nMatriz de distancias (primeras 5 filas):")
print(dist_matrix_df.head())
print(f"\n¡Listo! La matriz completa ha sido guardada en el archivo: '{output_file}'")