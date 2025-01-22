import geopandas as gpd

# Ruta del archivo shapefile
ruta_shapefile = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Rasteriza_lul_igm\lulc_actualizado.shp"

# Cargar el archivo shapefile
gdf = gpd.read_file(ruta_shapefile)

# Diccionario de asignación de valores
reemplazo_valores = {1: 8, 2: 1, 3: 2, 4: 3, 5: 9, 6: 10, 7: 12, 8: 13, 9: 11, 10: 7}

# Crear o actualizar la columna "class" basada en "Class"
gdf['class'] = gdf['class_2'].map(reemplazo_valores)

# Guardar los cambios en un nuevo archivo shapefile
ruta_salida = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Rasteriza_lul_igm\lulc_actualizado.shp"
gdf.to_file(ruta_salida)

print(f"El archivo actualizado se ha guardado en: {ruta_salida}")
