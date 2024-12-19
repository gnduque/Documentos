import rasterio
import numpy as np
import pandas as pd

def calculate_area(raster_path):
    with rasterio.open(raster_path) as src:
        # Leer la máscara del raster y la resolución espacial
        data = src.read(1)
        transform = src.transform
        
        # Determinar el tamaño de un píxel en kilómetros cuadrados (asumiendo una proyección en metros)
        pixel_size_x, pixel_size_y = transform[0], -transform[4]
        pixel_area = pixel_size_x * pixel_size_y / 1e6  # Convertir a km²
        
        # Calcular el total de píxeles
        total_pixels = data.size
        
        # Filtrar los valores de las clases 1 a 10
        class_mask = (data >= 1) & (data <= 10)
        class_data = data[class_mask]
        
        # Contar la cantidad de píxeles por clase
        unique_classes, counts = np.unique(class_data, return_counts=True)
        
        # Calcular el área por clase en km² y el porcentaje
        area_per_class = counts * pixel_area
        percentage_per_class = (counts / total_pixels) * 100
        
        return unique_classes, area_per_class, percentage_per_class

# Especificar las rutas de los archivos raster
raster_2009_2015 = "C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Clasifica_GEE/Clasifica_RF_CART_SVM/Raster_Results/LULC_2009_2015_RF.tif"
raster_2019_2024 = "C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Clasifica_GEE/Clasifica_RF_CART_SVM/Raster_Results/LULC_2019_2024_RF.tif"

# Calcular área y porcentaje para ambos rasters
classes_2009_2015, area_2009_2015, percentage_2009_2015 = calculate_area(raster_2009_2015)
classes_2019_2024, area_2019_2024, percentage_2019_2024 = calculate_area(raster_2019_2024)

# Crear un DataFrame para almacenar los resultados
df_2009_2015 = pd.DataFrame({
    'Clase': classes_2009_2015,
    'Área (km²)': area_2009_2015,
    'Porcentaje (%)': percentage_2009_2015,
    'Periodo': '2009-2015'
})

df_2019_2024 = pd.DataFrame({
    'Clase': classes_2019_2024,
    'Área (km²)': area_2019_2024,
    'Porcentaje (%)': percentage_2019_2024,
    'Periodo': '2019-2024'
})

# Concatenar ambos DataFrames
df_final = pd.concat([df_2009_2015, df_2019_2024], ignore_index=True)

# Guardar la tabla en un archivo CSV
output_path = "C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Matriz_cambios/Cambios_LULC/areas_clase.csv"
df_final.to_csv(output_path, index=False)

print(f"Los resultados han sido guardados en: {output_path}")
