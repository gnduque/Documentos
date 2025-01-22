import rasterio
import numpy as np
import pandas as pd

# Rutas de los rasters
classes_raster_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Clasifica_RF_CART_SVM\Raster_Results\LULC_2020_2022_RF.tif"
aod_raster_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Esenarios_AOD\Pandemia\AOD_2020-08-25_2020-08-30.tif"

# Leer ambos rasters
with rasterio.open(classes_raster_path) as classes_src, rasterio.open(aod_raster_path) as aod_src:
    # Leer datos
    classes_data = classes_src.read(1)
    aod_data = aod_src.read(1)
    
    # Verificar alineación de rasters
    if classes_src.shape != aod_src.shape:
        raise ValueError("Los rasters no tienen las mismas dimensiones.")
    if classes_src.transform != aod_src.transform:
        raise ValueError("Los rasters no están alineados espacialmente.")
    
# Obtener las clases únicas del primer raster
unique_classes = np.unique(classes_data)

# Calcular el valor medio de AOD para cada clase
results = {}
for cls in unique_classes:
    mask = classes_data == cls
    aod_values = aod_data[mask]
    # Reemplazar valores nulos (NaN) con 0
    aod_values = np.where(np.isnan(aod_values), 0, aod_values)
    mean_aod = np.mean(aod_values)
    results[cls] = mean_aod

# Crear un DataFrame con los resultados
df_results = pd.DataFrame(list(results.items()), columns=['Clase', 'Media de AOD'])

# Guardar la tabla en un archivo CSV
output_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\AOD_LULC\results\aod_results.csv"
df_results.to_csv(output_path, index=False)

print(f"Los resultados se han guardado en {output_path}")