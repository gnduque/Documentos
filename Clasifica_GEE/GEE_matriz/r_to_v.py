import ee
import geemap
import geopandas as gpd
from shapely.geometry import box
from tqdm import tqdm  # Para la barra de progreso
import pandas as pd  # Asegúrate de importar pandas si usas concat para GeoDataFrames

# Autenticación e inicialización de Google Earth Engine
ee.Authenticate()
ee.Initialize()

# IDs de los assets en Google Earth Engine
raster_asset_id = 'projects/modern-renderer-413302/assets/LULC_2009_2015_CART'
shapefile_asset_id = 'projects/modern-renderer-413302/assets/ecuador_borde_pol'

# Función para dividir el área en una cuadrícula
def split_geometry(geometry, rows, cols):
    """Divide una geometría en una cuadrícula de filas y columnas."""
    # Obtener los límites como una lista de coordenadas [xmin, ymin, xmax, ymax]
    bounds = geometry.bounds().coordinates().get(0).getInfo()

    # Extraer los valores mínimos y máximos
    xmin = bounds[0][0]
    ymin = bounds[0][1]
    xmax = bounds[2][0]
    ymax = bounds[2][1]

    # Calcular el ancho y la altura de cada subregión
    width = (xmax - xmin) / cols
    height = (ymax - ymin) / rows

    subregions = []
    for i in range(rows):
        for j in range(cols):
            subregion = box(
                xmin + j * width, ymax - (i + 1) * height,
                xmin + (j + 1) * width, ymax - i * height
            )
            subregions.append(subregion)
    return subregions

# Paso 1: Cargar la imagen y el shapefile desde los assets
image = ee.Image(raster_asset_id)
table = ee.FeatureCollection(shapefile_asset_id)

# Generar cuadrícula de subregiones (por ejemplo, 4x4)
geometry = table.geometry()
rows, cols = 4, 4
subregions = split_geometry(geometry, rows, cols)

# Lista para almacenar los resultados
gdfs = []

# Procesar cada subregión con una barra de progreso
with tqdm(total=len(subregions), desc="Procesando subregiones") as pbar:
    for i, subregion in enumerate(subregions):
        # Convertir subregión a geometría de Earth Engine
        try:
            coords = list(subregion.exterior.coords)  # Convertir las coordenadas a lista
            ee_subregion = ee.Geometry.Polygon([coords])  # Formato esperado por EE

            # Reducir la imagen a vectores en esta subregión
            vectors = image.reduceToVectors(
                geometry=ee_subregion,
                crs='EPSG:32717',
                scale=90,
                geometryType='polygon',
                labelProperty='value'
            )
            
            # Convertir a GeoDataFrame
            gdf = geemap.ee_to_gdf(vectors)
            gdfs.append(gdf)
        except Exception as e:
            print(f"Error procesando subregión {i + 1}: {e}")

        # Incrementar la barra de progreso
        pbar.update(1)

# Combinar todos los GeoDataFrames
combined_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))

# Guardar el shapefile combinado
output_shapefile = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\GEE_matriz\combined_vector_90.shp'
combined_gdf.to_file(output_shapefile)

print(f"Archivo vectorial combinado creado")
