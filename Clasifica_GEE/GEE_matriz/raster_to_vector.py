import ee
import geemap
import geopandas as gpd
from tqdm import tqdm  # Biblioteca para la barra de progreso

# Autenticación e inicialización de Google Earth Engine
ee.Authenticate()
ee.Initialize(project='aerial-sandbox-412207')

# IDs de los assets en Google Earth Engine (asegúrate de haberlos subido previamente)
raster_asset_id = 'projects/modern-renderer-413302/assets/LULC_2009_2015_CART'
shapefile_asset_id = 'projects/modern-renderer-413302/assets/ecuador_borde_pol'

# Barra de progreso inicial
steps = ["Cargar assets", "Reducir a vectores", "Convertir a GeoDataFrame", "Guardar Shapefile"]
with tqdm(total=len(steps), desc="Progreso del script", bar_format="{l_bar}{bar} [ {n_fmt}/{total_fmt} pasos ]") as pbar:
    
    # Paso 1: Cargar la imagen y el shapefile desde los assets
    image = ee.Image(raster_asset_id)
    table = ee.FeatureCollection(shapefile_asset_id)
    pbar.update(1)

    # Paso 2: Reducir la imagen a vectores
    vectors = image.reduceToVectors(
        geometry=table.geometry(),
        crs='EPSG:32717',  # Ajusta el CRS según sea necesario
        scale=3000,
        geometryType='polygon',
        labelProperty='value'
    )
    pbar.update(1)

    # Paso 3: Convertir los vectores a GeoDataFrame
    gdf = geemap.ee_to_gdf(vectors)
    pbar.update(1)

    # Paso 4: Guardar el GeoDataFrame como un shapefile
    output_shapefile = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Clasifica_RF_CART_SVM\Raster_Results\vector_3000.shp'
    gdf.to_file(output_shapefile)
    pbar.update(1)

print(f"Archivo vectorial creado en {output_shapefile}")
