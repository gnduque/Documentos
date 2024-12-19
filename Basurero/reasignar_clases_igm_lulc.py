import geopandas as gpd

# Ruta del archivo shapefile
ruta_shapefile = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Rasteriza_lul_igm\lulc_comparar_corregido.shp"

# Cargar el archivo shapefile
gdf = gpd.read_file(ruta_shapefile)

# Diccionario de asignación de valores
reemplazo_valores = {1: 9, 2: 8, 3: 7, 4: 6, 5: 5, 6: 4, 7: 3, 8: 2, 9: 10, 10: 1}

# Crear o actualizar la columna "class" basada en "Class"
gdf['class'] = gdf['Class'].map(reemplazo_valores)

# Guardar los cambios en un nuevo archivo shapefile
ruta_salida = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Rasteriza_lul_igm\lulc_actualizado.shp"
gdf.to_file(ruta_salida)

print(f"El archivo actualizado se ha guardado en: {ruta_salida}")
