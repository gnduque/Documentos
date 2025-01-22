import rasterio
import numpy as np
import pandas as pd

# Rutas de los rasters
#classes_raster_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Clasifica_RF_CART_SVM\Raster_Results\LULC_2020_2022_RF.tif"
classes_raster_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Clasifica_RF_CART_SVM\Raster_Results\LULC_2010_2014_RF.tif"
aod_raster_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Esenarios_AOD\Periodos_estacional\AOD_2013-07-01_2013-09-30.tif"

# Leer ambos rasters
with rasterio.open(classes_raster_path) as classes_src, rasterio.open(aod_raster_path) as aod_src:
    classes_data = classes_src.read(1)
    aod_data = aod_src.read(1)
    
    if classes_src.shape != aod_src.shape:
        raise ValueError("Los rasters no tienen las mismas dimensiones.")
    if classes_src.transform != aod_src.transform:
        raise ValueError("Los rasters no están alineados espacialmente.")

# Obtener las clases únicas del primer raster
unique_classes = np.unique(classes_data)

# Calcular el valor medio de AOD para cada clase
results = []
for cls in unique_classes:
    mask = classes_data == cls
    aod_values = aod_data[mask]
    valid_values = aod_values[np.isfinite(aod_values)]
    
    if len(valid_values) > 0:
        mean_aod = np.mean(valid_values)
    else:
        mean_aod = np.nan  # Usar NaN para clases sin datos válidos
    
    results.append((cls, mean_aod))

# Crear un DataFrame con los resultados
df_results = pd.DataFrame(results, columns=['Clase', 'Media de AOD'])

# Guardar la tabla en un archivo CSV
output_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\AOD_LULC\results\aod_results.csv"
df_results.to_csv(output_path, index=False)

print(f"Los resultados se han guardado en {output_path}")
