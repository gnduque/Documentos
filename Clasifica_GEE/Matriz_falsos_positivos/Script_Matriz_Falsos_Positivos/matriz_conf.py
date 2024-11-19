import rasterio
import geopandas as gpd
from rasterio.features import shapes
import numpy as np
from shapely.geometry import shape

# Leer el archivo raster y obtener las transformaciones
raster_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasificación_GEE\Clasificación_RF_CART_SVM\Raster_Results\LULC_2009_2015_CART.tif'

with rasterio.open(raster_path) as src:
    band1 = src.read(1)  # Leer la primera banda
    transform = src.transform
    rows, cols = band1.shape

# Eliminar píxeles con valor cero
non_zero_coords = []
non_zero_values = []

for row in tqdm(range(rows), desc="Filtering non-zero pixels"):
    for col in range(cols):
        if band1[row, col] != 0:
            x, y = rasterio.transform.xy(transform, row, col, offset='center')
            non_zero_coords.append((x, y))
            non_zero_values.append(band1[row, col])

# Crear un GeoDataFrame con los píxeles no nulos
shapes = [box(x, y, x + transform.a, y - transform.e) for x, y in non_zero_coords]
raster_gdf = gpd.GeoDataFrame({'geometry': shapes, 'predicted': non_zero_values})
print("GeoDataFrame con pixeles no nulos listo")

# Leer el shapefile original con la propiedad 'class'
shapefile_path = '/content/drive/MyDrive/Mapas LULC/Capas/lulc_comparar.shp'
gdf = gpd.read_file(shapefile_path)
