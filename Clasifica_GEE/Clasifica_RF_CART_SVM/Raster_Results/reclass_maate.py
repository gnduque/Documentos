import rasterio
import numpy as np

# Ruta del archivo raster original y del archivo de salida
input_raster = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Clasifica_RF_CART_SVM\Raster_Results\LULC_2020_2022_SVM.tif"
output_raster = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Clasifica_RF_CART_SVM\Raster_Results\LULC_2020_2022_SVM_reclass_maate.tif"

# Abrir el archivo raster
with rasterio.open(input_raster) as src:
    data = src.read(1)  # Leer la primera banda
    meta = src.meta  # Copiar metadatos

# Reclasificación de valores
data_reclassified = np.where((data == 8) | (data == 9), 4, data)
data_reclassified = np.where((data == 10) | (data == 11), 5, data_reclassified)
data_reclassified = np.where((data == 12) | (data == 13), 6, data_reclassified)

# Actualizar los metadatos para el nuevo archivo
meta.update(dtype=rasterio.int32)

# Guardar el nuevo raster reclasificado
with rasterio.open(output_raster, 'w', **meta) as dst:
    dst.write(data_reclassified.astype(rasterio.int32), 1)
