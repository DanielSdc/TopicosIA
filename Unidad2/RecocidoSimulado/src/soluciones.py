import numpy as np
import random
import math


def recocido_simulado(solucion_inicial, matriz_distancias, iteraciones_sin_mejora, temperatura_inicial, 
                      enfriamiento, temperatura_minima, iteraciones_por_temperatura):
    
    solucion_actual = solucion_inicial
    mejor_solucion = solucion_actual
    costo_actual = calcular_costo_solucion(solucion_actual, matriz_distancias)
    mejor_costo = costo_actual
    temperatura = temperatura_inicial

    iteraciones=0

    # Criterio de parada por temperatura
    while temperatura > temperatura_minima:

        #Criterio de parada por iteraciones sin mejora
        if iteraciones >= iteraciones_sin_mejora:
            print(f"No se encontraron mejoras en las últimas {iteraciones_sin_mejora} iteraciones. Terminando recocido simulado.")
            break

        # Generar varias soluciones vecinas por cada temperatura
        for _ in range(iteraciones_por_temperatura):

            # Generar una nueva solución vecina y se obtiene el costo con la funcion objetivo
            vecino_nuevo = generar_vecino(solucion_actual)
            costo_vecino = calcular_costo_solucion(vecino_nuevo, matriz_distancias)

            #Obtener la diferencia de costos
            delta = costo_vecino - costo_actual

            # Si la nueva solución es mejor, o si se acepta por probabilidad
            if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperatura):
                solucion_actual = vecino_nuevo
                costo_actual = costo_vecino
                
                # Actualizar la mejor solución encontrada
                if costo_actual < mejor_costo:
                    mejor_solucion = solucion_actual
                    mejor_costo = costo_actual
                    iteraciones = 0

        # Enfriar la temperatura
        temperatura *= enfriamiento
        iteraciones += 1

    return mejor_solucion, mejor_costo

# Funcion para generar una solucion vecina
def generar_vecino(solucion):

    # Crear una copia de la solución actual para generar un vecino a partir de ella
    solucion_vecina = solucion.copy()

    # Encontrar los indices de las tiendas en la solucion
    indices_tiendas = [i for i, nodo in enumerate(solucion_vecina) if not es_cd(nodo)]


    #Generar una solucion vecina de dos formas distintas
    if random.random() < 0.5:
        # Intercambiar dos tiendas aleatorias
        i, j = random.sample(indices_tiendas, 2)
        solucion_vecina[i], solucion_vecina[j] = solucion_vecina[j], solucion_vecina[i]
        return solucion_vecina
    else:
        #Mover una tienda a una posicion diferente
        i = random.choice(indices_tiendas)
        tienda = solucion_vecina.pop(i)

        #Generar una lista de posiciones validas (entre dos tiendas, entre tienda y CD ó entre dos CDs iguales)
        posiciones_validas = []
        for j in range(1, len(solucion_vecina)):
            izquierda = solucion_vecina[j - 1]
            derecha = solucion_vecina[j]

            
            if es_cd(izquierda) and es_cd(derecha):
                # Posicion valida si ambos son CDs y son el mismo CD
                if izquierda == derecha:
                    posiciones_validas.append(j)
                else:
                    continue
            else:
                # Posicion valida si al menos uno no es CD
                posiciones_validas.append(j)
        # Elegir una posicion valida aleatoria para insertar la tienda
        posicion = random.choice(posiciones_validas)
        solucion_vecina.insert(posicion, tienda)
        return solucion_vecina
    
    

#Funcion para asignar tiendas a su CD mas cercano en base a coordenadas euclidianas
def asignar_tiendas_cercanas(cds_df, tiendas_df):

    # Obtener las coordenadas de CDs
    coords_cds = cds_df[['Coordenada X', 'Coordenada Y']].values.astype(float)
    asignaciones = {cd_id: [] for cd_id in cds_df['ID']}

    #Iterar sobre cada tienda y asignarla al CD más cercano
    for _, tienda in tiendas_df.iterrows():

        # Obtener las coordenadas de la tienda
        coords_tienda = tienda[['Coordenada X', 'Coordenada Y']].values.astype(float)

        #Calcular distancias euclidianas entre la tienda y todos los CDs
        distancias = np.linalg.norm(coords_cds - coords_tienda, axis=1)

        #Buscar el CD más cercano y asignar la tienda
        cd_cercano_id = cds_df.iloc[np.argmin(distancias)]['ID']
        asignaciones[cd_cercano_id].append(tienda['ID'])

    return asignaciones

#Funcion para generar una solucion inicial
def generar_solucion_inicial(cds_df, tiendas_df):

    # Obtener las asignaciones de tiendas a CDs
    asignaciones = asignar_tiendas_cercanas(cds_df, tiendas_df)

    solucion_inicial = []
    
    cd_ids = sorted(asignaciones.keys())

    #Generar una ruta aleatoria para cada CD y sus tiendas asignadas
    for cd_id in cd_ids:
        ruta_tiendas = asignaciones.get(cd_id, [])
        if ruta_tiendas:
            solucion_inicial.append(cd_id)
            random.shuffle(ruta_tiendas)
            solucion_inicial.extend(ruta_tiendas)
            solucion_inicial.append(cd_id)

    return solucion_inicial, asignaciones

#Funcion para calcular el costo total de una solucion dada la matriz de distancias
def calcular_costo_solucion(solucion, matriz_distancias):

    # Dividir la solucion en rutas basadas en CDs
    rutas = dividir_solucion_en_rutas(solucion)
    costo_total = 0.0

    # Iterar sobre cada ruta y sumar las distancias entre nodos consecutivos
    for ruta in rutas:
        for u, v in zip(ruta[:-1], ruta[1:]):
            costo_total += matriz_distancias[u-1, v-1]
    return costo_total


#Funcion auxiliar para dividir la solucion en rutas
def dividir_solucion_en_rutas(solucion):

    # Dividir el arreglo de solución en uno para cada CD y sus tiendas asignadas
    rutas: list[list[int]] = []
    ruta_actual: list[int] = []
    for nodo in solucion:
        if es_cd(nodo):
            if not ruta_actual:
                ruta_actual.append(nodo)
            else:
                ruta_actual.append(nodo)
                rutas.append(ruta_actual)
                ruta_actual = []
        else:
            if ruta_actual:
                ruta_actual.append(nodo)
            else:
                continue
    return rutas

#Funciones auxiliares para identificar tipo de nodo (CD o tienda)
def es_cd(nodo_id):
    return 1 <= nodo_id <= 10

def es_tienda(nodo_id):
    return nodo_id > 10
