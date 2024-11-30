import ee

# Inicializar la API de Google Earth Engine
ee.Initialize()

# Cargar la capa vectorial
vector_layer = ee.FeatureCollection('projects/modern-renderer-413302/assets/lulc_comparar')

# Cargar la geometría dentro de la cual se va a realizar la rasterización
geometry = ee.FeatureCollection('projects/modern-renderer-413302/assets/borde_raster')

# Convertir la colección de vectores en un raster usando el atributo 'Class'
raster = vector_layer.reduceToImage(
    properties=['Class'],  # Lista de propiedades a convertir en imágenes
    reducer=ee.Reducer.first()  # Reducer que define cómo manejar múltiples valores para un solo pixel
).clip(geometry)

# Especificar la resolución del raster
raster_final = raster.reproject(
    crs=raster.projection().crs(),
    scale=30
)

# Configurar la tarea de exportación para guardar el archivo en Google Drive
task = ee.batch.Export.image.toDrive(
    image=raster_final,
    description='export_raster_to_specific_folder',
    scale=30,
    region=geometry.geometry().bounds(),
    folder='EarthEngineExports',
    fileFormat='GeoTIFF',
    maxPixels=1e9  # Ajusta según la necesidad, hasta un límite razonable
)
