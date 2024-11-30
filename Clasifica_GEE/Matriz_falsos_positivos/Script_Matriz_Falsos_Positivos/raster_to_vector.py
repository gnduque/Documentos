import rasterio
import numpy as np
from shapely.geometry import shape, mapping
import geopandas as gpd
from rasterio.features import shapes
from tqdm import tqdm

# Ruta al archivo raster
raster_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Clasifica_RF_CART_SVM\Raster_Results\LULC_2009_2015_CART.tif'
# Ruta para el archivo vectorial de salida
output_shapefile = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Clasifica_RF_CART_SVM\Raster_Results\LULC_2009_2015_CART.shp'

# Abrir el archivo raster
with rasterio.open(raster_path) as src:
    image = src.read(1)
    mask = image != 0  # Máscara para ignorar los valores 0 si es necesario

    # Enumerar las formas con barra de progreso
    results = (
        {'properties': {'value': v}, 'geometry': s}
        for i, (s, v) 
        in tqdm(enumerate(shapes(image, mask=mask, transform=src.transform)), desc="Procesando raster")
    )

    # Crear GeoDataFrame desde las geometrías extraídas
    geoms = list(results)
    gdf = gpd.GeoDataFrame.from_features(geoms)
    
    # Guardar a archivo shapefile
    gdf.to_file(output_shapefile)

print(f"Vector file created at {output_shapefile}")
