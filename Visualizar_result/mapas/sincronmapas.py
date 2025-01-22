import folium
import ee
from folium.plugins import DualMap

# Inicializar Earth Engine
ee.Initialize()

# Obtener el URL de los tiles para una imagen
image1 = ee.Image("projects/modern-renderer-413302/assets/LULC_2009_2015_R")
map_id_dict1 = image1.getMapId({
    'min': 1,
    'max': 10,
    'palette': ['#ffffff', '#00FFFF', '#006400', '#00FF00', '#800000', '#808080', '#FFFF00', '#808000', '#FF00FF', '#AFEEEE']
})
lulc_2009_2015_url = map_id_dict1['tile_fetcher'].url_format

# Obtener el URL de los tiles para una imagen
image2 = ee.Image("projects/modern-renderer-413302/assets/LULC_2019_2024_R")
map_id_dict2 = image2.getMapId({
    'min': 1,
    'max': 10,
    'palette': ['#ffffff', '#00FFFF', '#006400', '#00FF00', '#800000', '#808080', '#FFFF00', '#808000', '#FF00FF', '#AFEEEE']
})
lulc_2019_2024_url = map_id_dict2['tile_fetcher'].url_format

# Cargar la imagen AOD y reclasificarla
aod3 = ee.Image("projects/modern-renderer-413302/assets/AOD_2009_2015_i")
aod_reclassified3 = aod3.expression(
    "b(0) <= 0 ? 1 : b(0) <= 0.04 ? 2 : b(0) <= 0.1 ? 3 : b(0) <= 0.15 ? 4 : b(0) <= 0.2 ? 5 : b(0) <= 0.3 ? 6 : b(0) <= 0.5 ? 7 : 8"
)

# Cargar la geometría
geometry = ee.FeatureCollection("projects/modern-renderer-413302/assets/ecuador_borde_pol")

# Enmascarar la imagen con la geometría
aod_clipped3 = aod_reclassified3.clipToCollection(geometry)

# Definir los parámetros de visualización
aod_vis_params = {
    'min': 1,
    'max': 8,
    'palette': ['#00FF00', '#7FFF00', '#FFFF00', '#FFD700', '#FFA500', '#FF4500', '#FF0000']
}

# Obtener el URL de los tiles
map_id_dict3 = aod_clipped3.getMapId(aod_vis_params)
aod_2009_2015_url = map_id_dict3['tile_fetcher'].url_format

# Cargar la imagen AOD y reclasificarla
aod4 = ee.Image("projects/modern-renderer-413302/assets/AOD_2019_2024_f")
aod_reclassified4 = aod4.expression(
    "b(0) <= 0 ? 1 : b(0) <= 0.04 ? 2 : b(0) <= 0.1 ? 3 : b(0) <= 0.15 ? 4 : b(0) <= 0.2 ? 5 : b(0) <= 0.3 ? 6 : b(0) <= 0.5 ? 7 : 8"
)

# Cargar la geometría
geometry = ee.FeatureCollection("projects/modern-renderer-413302/assets/ecuador_borde_pol")

# Enmascarar la imagen con la geometría
aod_clipped4 = aod_reclassified4.clipToCollection(geometry)

# Definir los parámetros de visualización
aod_vis_params = {
    'min': 1,
    'max': 8,
    'palette': ['#00FF00', '#7FFF00', '#FFFF00', '#FFD700', '#FFA500', '#FF4500', '#FF0000']
}

# Obtener el URL de los tiles
map_id_dict4 = aod_clipped4.getMapId(aod_vis_params)
aod_2019_2024_url = map_id_dict4['tile_fetcher'].url_format

# Crear un mapa dual
dual_map = DualMap(location=[-0.229, -78.52], zoom_start=12)

# Añadir capas al primer mapa
folium.TileLayer('OpenStreetMap').add_to(dual_map.m1)
folium.TileLayer(
    tiles=lulc_2009_2015_url,
    attr='Google Earth Engine',
    name='LULC 2009-2015'
).add_to(dual_map.m1)
folium.TileLayer(
    tiles=aod_2009_2015_url,
    attr='Google Earth Engine',
    name='AOD 2009-2015'
).add_to(dual_map.m1)

# Añadir capas al segundo mapa
folium.TileLayer('OpenStreetMap').add_to(dual_map.m2)
folium.TileLayer(
    tiles=lulc_2019_2024_url,
    attr='Google Earth Engine',
    name='LULC 2019-2024'
).add_to(dual_map.m2)
folium.TileLayer(
    tiles=aod_2019_2024_url,
    attr='Google Earth Engine',
    name='AOD 2019-2024'
).add_to(dual_map.m2)

# Añadir control de capas a ambos mapas
folium.LayerControl().add_to(dual_map.m1)
folium.LayerControl().add_to(dual_map.m2)

# Guardar el mapa en un archivo HTML en la ruta especificada
output_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Visualizar_result\mapas\comparacion_de_mapas.html'
dual_map.save(output_path)