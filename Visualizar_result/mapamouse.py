import ee
import geemap

# Inicializar Earth Engine
ee.Initialize(project='aerial-sandbox-412207')

# Cargar datos de Earth Engine
dataset = ee.Image("projects/modern-renderer-413302/assets/LULC_2009_2015_i").reproject(crs='EPSG:4326', scale=30)

# Parámetros de visualización para la capa de Earth Engine
vis_params = {
    'min': 1,
    'max': 10,
    'palette': ['#ffffff', '#00FFFF', '#006400', '#00FF00', '#800000', '#808080', '#FFFF00', '#808000', '#FF00FF', '#AFEEEE']
}

# Crear un mapa base con geemap centrado en las coordenadas especificadas
mapa = geemap.Map(center=[-0.229, -78.52], zoom=12)

# Añadir una capa de visualización de Google Satélite
mapa.add_basemap('SATELLITE')

# Añadir la capa de Earth Engine al mapa
mapa.addLayer(dataset, vis_params, 'LULC 2009-2015')

# Cargar el mapa raster desde Earth Engine y reclasificar los píxeles
raster = ee.Image("projects/modern-renderer-413302/assets/AOD_2009_2015")
raster_reclassified = raster.expression(
    "b(0) <= 0 ? 1 : b(0) <= 0.04 ? 2 : b(0) <= 0.1 ? 3 : b(0) <= 0.15 ? 4 : b(0) <= 0.2 ? 5 : b(0) <= 0.3 ? 6 : b(0) <= 0.5 ? 7 : 8"
)

# Cargar la geometría para cortar la capa raster
geometry = ee.FeatureCollection("projects/modern-renderer-413302/assets/ecuador_borde_pol")

# Cortar la capa raster con la geometría especificada
raster_clipped = raster_reclassified.clipToCollection(geometry)

# Parámetros de visualización para el raster reclasificado y cortado
raster_vis_params = {
    'min': 1,
    'max': 8,
    'palette': ['#00FF00', '#7FFF00', '#FFFF00', '#FFD700', '#FFA500', '#FF4500', '#FF0000']
}

# Añadir la capa raster reclasificada y cortada al mapa
mapa.addLayer(raster_clipped, raster_vis_params, 'AOD Inicial Reclasificado')

# Añadir el control de capas
mapa.addLayerControl()

# Añadir la herramienta Inspector
mapa.add_inspector()

# Guardar el mapa
mapa.to_html(r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Visualizar_result\mapa_interactivo.html")

print("El mapa interactivo ha sido guardado correctamente con el panel de capas funcional y el inspector de valores.")