# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 21:17:42 2024

@author: ADMIN
"""
import geopandas as gpd
import pandas as pd

# Rutas a los archivos shapefile
ruta_bananera = r"C:\Users\ADMIN\Desktop\TESIS\Matriz_falsos_positivos\bananeras_ec.shp"
ruta_rf = r"C:\Users\ADMIN\Desktop\TESIS\Matriz_falsos_positivos\RF_vector.shp"

# Cargar archivos shapefile como GeoDataFrames
bananera_gdf = gpd.read_file(ruta_bananera)
rf_gdf = gpd.read_file(ruta_rf)

# Realizar la intersección entre los GeoDataFrames
interseccion_gdf = gpd.overlay(bananera_gdf, rf_gdf, how='intersection')

# Calcular el área para cada polígono
interseccion_gdf['area'] = interseccion_gdf.geometry.area

# Exportar la tabla de atributos como un archivo CSV
ruta_salida_csv = r"C:\Users\ADMIN\Desktop\TESIS\Matriz_falsos_positivos\interseccion_atributos_con_area.csv"
interseccion_gdf.to_csv(ruta_salida_csv, index=False)

print("Tabla de atributos exportada como CSV exitosamente.")


# Leer el archivo CSV de salida
ruta_csv = r"C:\Users\ADMIN\Desktop\TESIS\Matriz_falsos_positivos\interseccion_atributos_con_area.csv"
data = pd.read_csv(ruta_csv)

# Calcular el área total de la intersección de los polígonos
area_total = data['area'].sum() /10000000

# Filtrar los datos según las condiciones para cada categoría
verdaderos_positivos = data[data['class_1'] == data['class_2']]
falsos_positivos = data[(data['class_1'] != 9) & (data['class_2'] == 9)]
verdaderos_negativos = data[(data['class_1'] == 9) & (data['class_2'] != 9)]
falsos_negativos = data[(data['class_1'] !=  9) & (data['class_2'] != 9)]

# Calcular el área total para cada categoría
area_vp = verdaderos_positivos['area'].sum() /10000000
area_fp = falsos_positivos['area'].sum() /10000000
area_vn = verdaderos_negativos['area'].sum() /10000000
area_fn = falsos_negativos['area'].sum() /10000000

# Calcular el porcentaje de área para cada categoría
porcentaje_vp = (area_vp / area_total) * 100
porcentaje_fp = (area_fp / area_total) * 100
porcentaje_vn = (area_vn / area_total) * 100
porcentaje_fn = (area_fn / area_total) * 100

# Crear la tabla de doble entrada con los resultados
tabla_resultados = pd.DataFrame({
    '': ['Verdaderos Positivos', 'Falsos Positivos', 'Verdaderos Negativos', 'Falsos Negativos'],
    'Área Total (Km^2)': [area_vp, area_fp, area_vn, area_fn],
    'Porcentaje del Área Total (%)': [porcentaje_vp, porcentaje_fp,porcentaje_vn, porcentaje_fn]
})
# Imprimir la tabla de resultados
print(tabla_resultados)