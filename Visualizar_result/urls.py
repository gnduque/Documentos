import ee

# Inicializar Earth Engine
ee.Initialize()

# Obtener el URL de los tiles para una imagen
image = ee.Image("projects/modern-renderer-413302/assets/LULC_2009_2015_i")
map_id_dict = image.getMapId({
    'min': 1,
    'max': 10,
    'palette': ['#ffffff', '#00FFFF', '#006400', '#00FF00', '#800000', '#808080', '#FFFF00', '#808000', '#FF00FF', '#AFEEEE']
})
tile_url = map_id_dict['tile_fetcher'].url_format
print(tile_url)

# Obtener el URL de los tiles para una imagen
image = ee.Image("projects/modern-renderer-413302/assets/LULC_2019_2024_F")
map_id_dict = image.getMapId({
    'min': 1,
    'max': 10,
    'palette': ['#ffffff', '#00FFFF', '#006400', '#00FF00', '#800000', '#808080', '#FFFF00', '#808000', '#FF00FF', '#AFEEEE']
})
tile_url = map_id_dict['tile_fetcher'].url_format
print(tile_url)


# Cargar la imagen AOD y reclasificarla
aod = ee.Image("projects/modern-renderer-413302/assets/AOD_2009_2015")
aod_reclassified = aod.expression(
    "b(0) <= 0 ? 1 : b(0) <= 0.04 ? 2 : b(0) <= 0.1 ? 3 : b(0) <= 0.15 ? 4 : b(0) <= 0.2 ? 5 : b(0) <= 0.3 ? 6 : b(0) <= 0.5 ? 7 : 8"
)

# Cargar la geometría
geometry = ee.FeatureCollection("projects/modern-renderer-413302/assets/ecuador_borde_pol")

# Enmascarar la imagen con la geometría
aod_clipped = aod_reclassified.clipToCollection(geometry)

# Definir los parámetros de visualización
aod_vis_params = {
    'min': 1,
    'max': 8,
    'palette': ['#00FF00', '#7FFF00', '#FFFF00', '#FFD700', '#FFA500', '#FF4500', '#FF0000']
}

# Obtener el URL de los tiles
map_id_dict = aod_clipped.getMapId(aod_vis_params)
tile_url = map_id_dict['tile_fetcher'].url_format
print(tile_url)

# Cargar la imagen AOD y reclasificarla
aod = ee.Image("projects/modern-renderer-413302/assets/AOD_2019_2024")
aod_reclassified = aod.expression(
    "b(0) <= 0 ? 1 : b(0) <= 0.04 ? 2 : b(0) <= 0.1 ? 3 : b(0) <= 0.15 ? 4 : b(0) <= 0.2 ? 5 : b(0) <= 0.3 ? 6 : b(0) <= 0.5 ? 7 : 8"
)

# Cargar la geometría
geometry = ee.FeatureCollection("projects/modern-renderer-413302/assets/ecuador_borde_pol")

# Enmascarar la imagen con la geometría
aod_clipped = aod_reclassified.clipToCollection(geometry)

# Definir los parámetros de visualización
aod_vis_params = {
    'min': 1,
    'max': 8,
    'palette': ['#00FF00', '#7FFF00', '#FFFF00', '#FFD700', '#FFA500', '#FF4500', '#FF0000']
}

# Obtener el URL de los tiles
map_id_dict = aod_clipped.getMapId(aod_vis_params)
tile_url = map_id_dict['tile_fetcher'].url_format
print(tile_url)