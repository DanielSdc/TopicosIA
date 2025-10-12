from src.cargar_data import cargar_coordenadas, cargar_matriz
from src.visualizacion import mapear_coordenadas, mapear_asignaciones, mapear_solucion
from src.soluciones import generar_solucion_inicial, calcular_costo_solucion, recocido_simulado
import numpy as np
def main():
    
    #Cargar datos de CDs y tiendas en dataframes separados para mapear
    cds_df, tiendas_df = cargar_coordenadas()

    #Mapear las coordenadas iniciales
    mapear_coordenadas(cds_df, tiendas_df)

    #Asignar tiendas a CDs y generar solucion inicial
    solucion_inicial, asignaciones = generar_solucion_inicial(cds_df, tiendas_df)

    #Mapear CDs y sus tiendas asignadas
    mapear_asignaciones(cds_df, tiendas_df, asignaciones)

    #Mapear solucion inicial
    mapear_solucion(solucion_inicial, cds_df, tiendas_df)

    matriz_distancias = None
    try:
        matriz_distancias = np.array(cargar_matriz())
    except Exception as e:
        print("Error al cargar matriz de distancias:", e)
        return
    
    # Calcular costo de la solucion inicial
    costo = calcular_costo_solucion(solucion_inicial, matriz_distancias)
    print(f"Costo de la solución inicial: {costo:.2f} km")
    
    #Iniciar Recocido simulado indicando los parametros deseados
    mejor_solucion, mejor_costo = recocido_simulado(solucion_inicial, matriz_distancias, iteraciones_sin_mejora=500, 
                                                    temperatura_inicial=10.0, enfriamiento=0.99, temperatura_minima=0.001, 
                                                    iteraciones_por_temperatura=1000)
    
    #Mostrar el mejor costo y mapear la mejor solucion encontrada
    print(f"Mejor costo encontrado: {mejor_costo:.2f} km")
    mapear_solucion(mejor_solucion, cds_df, tiendas_df, filename="4_mapa_mejor_solucion.html")

if __name__ == "__main__":
    main()