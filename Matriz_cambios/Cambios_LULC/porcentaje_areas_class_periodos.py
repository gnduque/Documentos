import rasterio
import numpy as np
import pandas as pd
import os

def calculate_area(raster_path):
    try:
        with rasterio.open(raster_path) as src:
            data = src.read(1)
            transform = src.transform
            pixel_size_x, pixel_size_y = transform[0], -transform[4]
            pixel_area = pixel_size_x * pixel_size_y / 1e6
            
            total_pixels = np.count_nonzero(data)
            
            # Filtrar las clases relevantes
            relevant_classes = [1, 2, 3, 7, 8, 9, 10, 11, 12, 13]
            class_mask = np.isin(data, relevant_classes)
            class_data = data[class_mask]
            
            if class_data.size == 0:
                print(f"No se encontraron clases relevantes en {raster_path}")
                return np.array([]), np.array([]), np.array([])
            
            unique_classes, counts = np.unique(class_data, return_counts=True)
            area_per_class = counts * pixel_area
            percentage_per_class = (counts / total_pixels) * 100
            
            return unique_classes, area_per_class, percentage_per_class
    except Exception as e:
        print(f"Error procesando {raster_path}: {e}")
        return np.array([]), np.array([]), np.array([])


# Verificar la existencia de los archivos raster
raster_2010_2013 = "C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Clasifica_GEE/Clasifica_RF_CART_SVM/Raster_Results/LULC_2010_2014_RF.tif"
raster_2020_2022 = "C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Clasifica_GEE/Clasifica_RF_CART_SVM/Raster_Results/LULC_2020_2022_RF.tif"

if not os.path.exists(raster_2010_2013):
    raise FileNotFoundError(f"Archivo no encontrado: {raster_2010_2013}")
if not os.path.exists(raster_2020_2022):
    raise FileNotFoundError(f"Archivo no encontrado: {raster_2020_2022}")

# Calcular área y porcentaje para ambos rasters
classes_2010_2013, area_2010_2013, percentage_2010_2013 = calculate_area(raster_2010_2013)
classes_2020_2022, area_2020_2022, percentage_2020_2022 = calculate_area(raster_2020_2022)

# Validar que los resultados no estén vacíos
if classes_2010_2013.size > 0 and classes_2020_2022.size > 0:
    # Crear DataFrames para cada periodo
    df_2010_2013 = pd.DataFrame({
        'Clase': classes_2010_2013,
        'Área (km²)': area_2010_2013,
        'Porcentaje (%)': percentage_2010_2013,
        'Periodo': '2010-2013'
    })

    df_2020_2022 = pd.DataFrame({
        'Clase': classes_2020_2022,
        'Área (km²)': area_2020_2022,
        'Porcentaje (%)': percentage_2020_2022,
        'Periodo': '2020-2022'
    })

    # Concatenar ambos DataFrames
    df_final = pd.concat([df_2010_2013, df_2020_2022], ignore_index=True)

    # Guardar la tabla en un archivo CSV
    output_path = "C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Matriz_cambios/Cambios_LULC/areas_clase.csv"
    df_final.to_csv(output_path, index=False)
    print(f"Los resultados han sido guardados en: {output_path}")
else:
    print("No se generaron resultados debido a problemas con los datos de entrada.")
