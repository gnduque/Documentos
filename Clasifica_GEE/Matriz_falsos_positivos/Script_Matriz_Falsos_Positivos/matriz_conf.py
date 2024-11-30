import rasterio
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import box
from tqdm import tqdm
from rasterio.transform import xy
from sklearn.metrics import confusion_matrix

# Leer el archivo raster y obtener las transformaciones

with rasterio.open(raster_path) as src:
    band1 = src.read(1)  # Leer la primera banda
    transform = src.transform
    rows, cols = band1.shape

# Función para procesar bloques del raster
def process_block(start_row, end_row):
    non_zero_coords = []
    non_zero_values = []
    for row in range(start_row, end_row):
        for col in range(cols):
            if band1[row, col] != 0:
                x, y = xy(transform, row, col, offset='center')
                non_zero_coords.append((x, y))
                non_zero_values.append(band1[row, col])
    return non_zero_coords, non_zero_values

# Procesar en bloques y recopilar resultados
block_size = 1000
all_non_zero_coords = []
all_non_zero_values = []

for start_row in tqdm(range(0, rows, block_size), desc="Filtrando píxeles no nulos"):
    end_row = min(start_row + block_size, rows)
    non_zero_coords, non_zero_values = process_block(start_row, end_row)
    all_non_zero_coords.extend(non_zero_coords)
    all_non_zero_values.extend(non_zero_values)

# Crear un GeoDataFrame con los píxeles no nulos con barra de progreso
shapes = []
for coord in tqdm(all_non_zero_coords, desc="Creando GeoDataFrame"):
    x, y = coord
    shapes.append(box(x, y, x + transform.a, y - transform.e))

raster_gdf = gpd.GeoDataFrame({'geometry': shapes, 'predicted': all_non_zero_values})

print("GeoDataFrame con píxeles no nulos listo")

# Guardar el GeoDataFrame como un archivo Shapefile
shapefile_output_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Clasifica_RF_CART_SVM\raster_non_zero_pixels.shp'
raster_gdf.to_file(shapefile_output_path)

print(f"Shapefile guardado en: {shapefile_output_path}")

# Leer el shapefile original con la propiedad 'class'
shapefile_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Clasifica_RF_CART_SVM\lulc_comparar.shp'
gdf = gpd.read_file(shapefile_path)

# Realizar la intersección
intersection = gpd.overlay(raster_gdf, gdf, how='intersection')

# Convertir las clases en valores enteros (si no lo están ya)
intersection['class'] = intersection['class'].astype(int)
intersection['predicted'] = intersection['predicted'].astype(int)

# Calcular el área de cada geometría en metros cuadrados
intersection['area'] = intersection['geometry'].area

# Guardar la intersección en un archivo Shapefile
intersection_output_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Clasifica_RF_CART_SVM\intersection_result.shp'
intersection.to_file(intersection_output_path)

print(f"Shapefile de intersección guardado en: {intersection_output_path}")

# Guardar la intersección en un archivo CSV
csv_output_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Clasifica_RF_CART_SVM\intersection_result.csv'
intersection[['geometry', 'area', 'class', 'predicted']].to_csv(csv_output_path, index=False)

print(f"Archivo CSV de intersección guardado en: {csv_output_path}")

# Calcular la matriz de confusión multiclase
conf_matrix = confusion_matrix(intersection['class'], intersection['predicted'], labels=range(1, 11))

# Inicializar los contadores para cada clase
TP = []
FN = []
FP = []
TN = []
area_TP = []
area_FN = []
area_FP = []
area_TN = []
percentage_TP = []
percentage_FN = []
percentage_FP = []
percentage_TN = []

total_area = intersection['area'].sum()

for i in range(len(conf_matrix)):
    tp_mask = (intersection['class'] == i + 1) & (intersection['predicted'] == i + 1)
    fn_mask = (intersection['class'] == i + 1) & (intersection['predicted'] != i + 1)
    fp_mask = (intersection['class'] != i + 1) & (intersection['predicted'] == i + 1)
    tn_mask = (intersection['class'] != i + 1) & (intersection['predicted'] != i + 1)

    tp_area = intersection[tp_mask]['area'].sum()
    fn_area = intersection[fn_mask]['area'].sum()
    fp_area = intersection[fp_mask]['area'].sum()
    tn_area = intersection[tn_mask]['area'].sum()

    TP.append(tp_area)
    FN.append(fn_area)
    FP.append(fp_area)
    TN.append(tn_area)

    area_TP.append(intersection[tp_mask].shape[0])
    area_FN.append(intersection[fn_mask].shape[0])
    area_FP.append(intersection[fp_mask].shape[0])
    area_TN.append(intersection[tn_mask].shape[0])

    percentage_TP.append(tp_area / total_area * 100)
    percentage_FN.append(fn_area / total_area * 100)
    percentage_FP.append(fp_area / total_area * 100)
    percentage_TN.append(tn_area / total_area * 100)

# Crear un DataFrame con los valores, las áreas y los porcentajes
results = pd.DataFrame({
    'Class': range(1, len(conf_matrix) + 1),
    'TP': TP,
    'FN': FN,
    'FP': FP,
    'TN': TN,
    'Area_TP': area_TP,
    'Area_FN': area_FN,
    'Area_FP': area_FP,
    'Area_TN': area_TN,
    'Percentage_TP': percentage_TP,
    'Percentage_FN': percentage_FN,
    'Percentage_FP': percentage_FP,
    'Percentage_TN': percentage_TN
})

# Guardar los resultados en un archivo Excel
output_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Clasifica_RF_CART_SVM\confusion_matrix_results.xlsx'
with pd.ExcelWriter(output_path) as writer:
    pd.DataFrame(conf_matrix, index=range(1, len(conf_matrix) + 1), columns=range(1, len(conf_matrix) + 1)).to_excel(writer, sheet_name='Confusion Matrix')
    results.to_excel(writer, sheet_name='Metrics')

print(f"Resultados guardados en: {output_path}")
