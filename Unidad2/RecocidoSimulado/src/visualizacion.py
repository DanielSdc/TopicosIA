import folium
import pandas as pd
from config import OUTPUT_DIR, CD_COLOR, TIENDA_COLOR
import os
import webbrowser
LAT_COL = 'Coordenada Y'
LON_COL = 'Coordenada X'
NOMBRE_COL = 'Nombre'
ID_COL = 'ID'


# Funcion para mapear coordenadas iniciales
def mapear_coordenadas(cds_df, tiendas_df, filename="1_mapa_inicial_coordenadas.html"):
    
    
    avg_lat = pd.concat([cds_df[LAT_COL], tiendas_df[LAT_COL]]).mean()
    avg_lon = pd.concat([cds_df[LON_COL], tiendas_df[LON_COL]]).mean()
    
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

    for _, row in cds_df.iterrows():
        folium.Marker(
            location=[row[LAT_COL], row[LON_COL]],
            popup=f"<strong>{row[NOMBRE_COL]}</strong>",
            icon=folium.Icon(color='darkred', icon='truck', prefix='fa')
        ).add_to(m)

    for _, row in tiendas_df.iterrows():
        folium.CircleMarker(
            location=[row[LAT_COL], row[LON_COL]],
            radius=5,
            popup=row[NOMBRE_COL],
            color=TIENDA_COLOR,
            fill=True,
            fill_color=TIENDA_COLOR
        ).add_to(m)

    filepath = os.path.join(OUTPUT_DIR, filename)
    m.save(filepath)
    print(f"Mapa coordenadas guardado en '{filepath}'")
    abrir_mapa(filepath)

# Funcion para mapear asignaciones de tiendas a CDs
def mapear_asignaciones(cds_df, tiendas_df, asignaciones, filename="2_mapa_asignaciones.html"):

    avg_lat = pd.concat([cds_df[LAT_COL], tiendas_df[LAT_COL]]).mean()
    avg_lon = pd.concat([cds_df[LON_COL], tiendas_df[LON_COL]]).mean()
    
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

    unique_cds = sorted(cds_df[ID_COL].unique())
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    for _, row in cds_df.iterrows():
        folium.Marker(
            location=[row[LAT_COL], row[LON_COL]],
            popup=f"<strong>{row[NOMBRE_COL]}</strong>",
            icon=folium.Icon(color='darkred', icon='truck', prefix='fa')
        ).add_to(m)

    for cd_id, tienda_id_asignada in asignaciones.items():
        color_index = unique_cds.index(cd_id)

        for tienda_id in tienda_id_asignada:
            tienda_row = tiendas_df[tiendas_df[ID_COL] == tienda_id].iloc[0]
            folium.CircleMarker(
                location=[tienda_row[LAT_COL], tienda_row[LON_COL]],
                radius=6,
                popup=f"{tienda_row[NOMBRE_COL]} (Asignada a CD {cd_id})",
                color=colors[color_index % len(colors)],
                fill=True,
                fill_opacity=0.8,
            ).add_to(m)

    filepath = os.path.join(OUTPUT_DIR, filename)
    m.save(filepath)
    print(f"Mapa solucion inicial guardado en'{filepath}'")
    abrir_mapa(filepath)

#Funcion para mapear solucion dadas las rutas
def mapear_solucion (solucion, cds_df, tiendas_df, filename="3_mapa_solucion_inicial.html"):

    avg_lat = pd.concat([cds_df[LAT_COL], tiendas_df[LAT_COL]]).mean()
    avg_lon = pd.concat([cds_df[LON_COL], tiendas_df[LON_COL]]).mean()
    
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    rutas = {}
    cd_actual = None
    nodos_ruta = []
    for node_id in solucion:
        if node_id <= 10:
            if not nodos_ruta:
                cd_actual = node_id
                nodos_ruta.append(cd_actual)
            else:
                nodos_ruta.append(cd_actual)
                if cd_actual not in rutas:
                    rutas[cd_actual] = []
                rutas[cd_actual].append(nodos_ruta)
                nodos_ruta = []
        else:
            nodos_ruta.append(node_id)

    color_idx = -1
    unique_cds_in_solution = sorted(list(rutas.keys()))

    for cd_id in unique_cds_in_solution:
        color_idx += 1
        lista_rutas = rutas[cd_id]
        for ruta in lista_rutas:
            coords_ruta = [coordenadas_id(n_id, cds_df, tiendas_df) for n_id in ruta]

            folium.PolyLine(locations=coords_ruta, color=colors[color_idx % len(colors)], weight=2.5, opacity=0.8).add_to(m)

            for i, node_id in enumerate(ruta):
                if not (i == 0 or i == len(ruta) - 1):
                    coords = coords_ruta[i]
                    folium.Marker(
                        location=coords,
                        popup=f"Parada {i}",
                        icon=folium.DivIcon(html=f'<div style="font-family: sans-serif; color: white; background-color: {colors[color_idx % len(colors)]}; border-radius: 50%; width: 20px; height: 20px; text-align: center; line-height: 20px; font-size: 12px;"><b>{i}</b></div>')
                    ).add_to(m)

    for _, row in cds_df.iterrows():
        folium.Marker(location=[row[LAT_COL], row[LON_COL]], popup=f"<strong>{row[NOMBRE_COL]}</strong>", icon=folium.Icon(color='darkred', icon='truck', prefix='fa')).add_to(m)

    filepath = os.path.join(OUTPUT_DIR, filename)
    m.save(filepath)
    print(f"Mapa de solución inicial guardado en '{filepath}'")
    abrir_mapa(filepath)
    

#Funcion auxiliar para abrir mapa en el navegador
def abrir_mapa(archivo):
    directorio_archivo = os.path.abspath(archivo)
    webbrowser.open(f'file://{directorio_archivo}')


#Funcion auxiliar para obtener coordenadas por ID 
def coordenadas_id(node_id, cds_df, tiendas_df):
    """Obtiene las coordenadas para un ID de nodo dado."""
    df_to_search = cds_df if node_id <= 10 else tiendas_df
    node_row = df_to_search[df_to_search[ID_COL] == node_id]
    if not node_row.empty:
        return node_row[[LAT_COL, LON_COL]].values[0]
    return None