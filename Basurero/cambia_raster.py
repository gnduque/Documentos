import rasterio
import numpy as np

# Ruta del raster inicial y del raster de salida
ruta_raster_inicial = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Rasteriza_lul_igm\rasterizado_lulc_igm_actual.tif"
ruta_raster_salida = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Rasteriza_lul_igm\rasterizado_lulc_igm_final.tif"

# Diccionario para reasignar valores
reemplazo_valores = {1: 8, 2: 1, 3: 2, 4: 3, 5: 9, 6: 10, 7: 12, 8: 13, 9: 11, 10: 7}

# Abrir el raster original
with rasterio.open(ruta_raster_inicial) as src:
    perfil = src.profile  # Guardar el perfil del raster original
    data = src.read(1)    # Leer la primera banda como un array numpy

# Reemplazar valores en el array
data_actualizada = np.copy(data)
for valor_inicial, valor_deseado in reemplazo_valores.items():
    data_actualizada[data == valor_inicial] = valor_deseado

# Guardar el nuevo raster
with rasterio.open(ruta_raster_salida, 'w', **perfil) as dst:
    dst.write(data_actualizada, 1)

print(f"El raster actualizado se ha guardado en: {ruta_raster_salida}")
