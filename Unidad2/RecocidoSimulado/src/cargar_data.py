import pandas as pd
import numpy as np
from config import DATA_DIR, DATOS_PUNTOS, MATRIZ_DISTANCIAS


def cargar_coordenadas():
    df = pd.read_excel(DATA_DIR + DATOS_PUNTOS)

    df.rename(columns={'Longitud_WGS84': 'Coordenada X', 'Latitud_WGS84': 'Coordenada Y'}, inplace=True)

    #Separar el dataframe segun el tipo
    cds_df = df[df['Tipo']=='Centro de Distribución'].copy()
    tiendas_df = df[df['Tipo']=='Tienda'].copy()

    #Asignar ID numerico CD 1-10, Tiendas 11-100
    cds_df['ID'] = cds_df['Nombre'].str.split().str[-1].astype(int)
    tiendas_df['ID'] = tiendas_df['Nombre'].str.split().str[-1].astype(int) + 10

    return cds_df, tiendas_df

def cargar_matriz():
    path = DATA_DIR + MATRIZ_DISTANCIAS
    
    # Leer la matriz directamente, con encabezado en la primera fila y primera columna como índice.
    df = pd.read_excel(path, header=0, index_col=0)
    
    # Convertir la matriz a formato numérico, reemplazando cualquier valor no numérico por NaN
    df_num = df.apply(pd.to_numeric, errors='coerce')
    
    # Verificar si la matriz es cuadrada y no tiene valores nulos
    if df_num.notnull().values.all() and df_num.shape[0] == df_num.shape[1]:
        return df_num.values.astype(float)
    
    # Si la matriz no es válida, lanzar un error
    raise ValueError(f"No se pudo convertir a una matriz cuadrada numérica la matriz de distancias en {path}. Revisa el formato del archivo.")