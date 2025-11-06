import numpy as np

# Formula de Haversine
# Calcula la distancia en kilómetros entre pares de coordenadas usando la formula de haversine.
# ===========================================================================================================
# Entrada:
#         Latitud y Longitud de dos puntos (en grados)
# Salida:
#         Distancia en km entre ambos puntos
# ===========================================================================================================
def _haversine_vectorized(lat1, lon1, lat2, lon2):
  
    # convertir a radianes
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    R = 6371.0088  # radio medio de la Tierra en km
    return R * c


def calcular_costos_vectorizado(X, datos_cultivos):

   # Funcion para calcular el costo para cada partícula en X basado en la distancia de cultivos a sensores.
   # ===========================================================================================================
   # Entrada:
   #        X: array (P, D) con P = número de partículas y D = 2*S (S sensores, lat/lon por sensor).
   #        datos_cultivos: array (N, 2) con [lat, lon] de cada cultivo.
   # Salida:
   #        costos: array (P,) con la suma de distancias (km) de cada cultivo al sensor más cercano
   #        definido por esa partícula.
    

    # Asegurar que sean arrays numpy
    X = np.asarray(X, dtype=float)
    coords = np.asarray(datos_cultivos, dtype=float)

    # P: número de partículas
    # D: número de dimensiones (2*S)
    P, D = X.shape
    S = D // 2  # sensores por partícula

    # Reestructurar X (P, S, 2) donde el último eje es (lat, lon)
    sensores = X.reshape(P, S, 2)
    crops = coords.astype(float)
    N = crops.shape[0]

    # Lista para acumular los costos
    costos = []

    for p in range(P):  # cada partícula
        sensores_p = sensores[p]  # (S, 2)
        dist_particula = []
        for c in range(N):  # cada cultivo
            lat_c, lon_c = crops[c]
            # calcular distancia de este cultivo a todos los sensores de esta partícula
            dists = _haversine_vectorized(lat_c, lon_c, sensores_p[:, 0], sensores_p[:, 1])
            # tomar el sensor más cercano
            dist_particula.append(np.min(dists))
        # costo total para esta partícula = suma de las distancias mínimas
        costos.append(np.sum(dist_particula))

    costos = np.array(costos)

    return costos
