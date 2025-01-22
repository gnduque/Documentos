import ee
import folium
import geemap

# Inicializar Earth Engine
ee.Initialize(project='modern-renderer-413302')

# Cargar datos de Earth Engine
dataset = ee.Image("projects/modern-renderer-413302/assets/LULC_2009_2015_R").reproject(crs='EPSG:4326', scale=30)

# Parámetros de visualización para la capa de Earth Engine
vis_params = {
    'min': 1,
    'max': 10,
    'palette': ['#ffffff', '#00FFFF', '#006400', '#00FF00', '#800000', '#808080', '#FFFF00', '#808000', '#FF00FF', '#AFEEEE']
}

# Crear un mapa base con folium centrado en las coordenadas especificadas
mapa = folium.Map(location=[-0.229, -78.52], zoom_start=12, control_scale=True)

# Añadir una capa de visualización de Google Satélite
google_satellite = folium.TileLayer(
    tiles='https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    attr='Google',
    name='Google Satellite',
    subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
    overlay=True
)
google_satellite.add_to(mapa)

# Convertir la imagen de Earth Engine a una capa de folium y añadirla al mapa
map_id_dict = dataset.getMapId(vis_params)
lulc_layer = folium.TileLayer(
    tiles=map_id_dict['tile_fetcher'].url_format,
    attr='Google Earth Engine',
    overlay=True,
    name='LULC 2009-2015'
)
lulc_layer.add_to(mapa)

# Cargar el mapa raster desde Earth Engine y reclasificar los píxeles
raster = ee.Image("projects/modern-renderer-413302/assets/AOD_2009_2015_i")
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

# Convertir el raster reclasificado y cortado a una capa de folium y añadirla al mapa
raster_map_id_dict = raster_clipped.getMapId(raster_vis_params)
aod_layer = folium.TileLayer(
    tiles=raster_map_id_dict['tile_fetcher'].url_format,
    attr='Google Earth Engine',
    overlay=True,
    name='AOD Inicial Reclasificado'
)
aod_layer.add_to(mapa)

# Añadir el control de capas
folium.LayerControl().add_to(mapa)

# Guardar el mapa
mapa.save(r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Visualizar_result\mapa_interactivo.html")

print("El mapa interactivo ha sido guardado correctamente con el panel de capas funcional.")
