import folium
import ee
from folium.plugins import DualMap
from folium import raster_layers

# Inicializar Earth Engine
ee.Initialize(project='modern-renderer-413302')
# Cargar la geometría máscara
geometry = ee.FeatureCollection("projects/modern-renderer-413302/assets/ecuador_borde_pol")


# Obtener el URL de los tiles para una imagen
image1 = ee.Image("projects/modern-renderer-413302/assets/LULC_2010_2014_RF")
imagen1_reclassified1 = image1.expression(
 "b(0) <= 1 ? 1 : b(0) <= 2 ? 2: b(0) <= 3 ? 3 : b(0) <= 7 ? 4 : b(0) <= 8 ? 5 : b(0) <= 9 ? 6 : b(0) <= 10 ? 7 : b(0) <= 11 ? 8 : b(0) <= 12 ? 9 : 10 "
)
# Enmascarar la imagen con la geometría
imagen1_clipped1 = imagen1_reclassified1.clipToCollection(geometry)

# Definir los parámetros de visualización
imagen1_vis_params = {
    'min': 1,
    'max': 10,
    'palette': ['#AEC3D4', '#132007', '#90ae41', '#00FFFF', '#fdf6f2', '#683401', '#CC0013', '#6F6F6F', '#ffff00', '#CDB33B']
}
# Obtener el URL de los tiles
map_id_dict1 = imagen1_clipped1.getMapId(imagen1_vis_params)
lulc_2010_2013_url = map_id_dict1['tile_fetcher'].url_format

# Obtener el URL de los tiles para una imagen
image2 = ee.Image("projects/modern-renderer-413302/assets/LULC_2020_2022_RF")
imagen2_reclassified2 = image2.expression(
 "b(0) <= 1 ? 1 : b(0) <= 2 ? 2: b(0) <= 3 ? 3 : b(0) <= 7 ? 4 : b(0) <= 8 ? 5 : b(0) <= 9 ? 6 : b(0) <= 10 ? 7 : b(0) <= 11 ? 8 : b(0) <= 12 ? 9 : 10 "
)
# Enmascarar la imagen con la geometría
imagen2_clipped2 = imagen2_reclassified2.clipToCollection(geometry)

# Definir los parámetros de visualización
imagen2_vis_params = {
    'min': 1,
    'max': 10,
    'palette': ['#AEC3D4', '#132007', '#90ae41', '#00FFFF', '#fdf6f2', '#683401', '#CC0013', '#6F6F6F', '#ffff00', '#CDB33B']
}
# Obtener el URL de los tiles
map_id_dict2 = imagen2_clipped2.getMapId(imagen2_vis_params)
lulc_2020_2022_url = map_id_dict2['tile_fetcher'].url_format

# Cargar la imagen AOD y reclasificarla
aod3 = ee.Image("projects/modern-renderer-413302/assets/AOD_2012")
aod_reclassified3 = aod3.expression(
"b(0) <= 0.08 ? 1 : b(0) <= 0.15 ? 2 : b(0) <= 0.24 ? 3 : b(0) <= 0.3 ? 4 : b(0) <= 0.4 ? 5 : b(0) <= 3 ? 6 : 7"
)
# Enmascarar la imagen con la geometría
aod_clipped3 = aod_reclassified3.clipToCollection(geometry)

# Definir los parámetros de visualización
aod_vis_params = {
    'min': 1,
    'max': 7,
    'palette': ['#2E7D32', '#64DD17', '#FFD600', '#FF8C00', '#D84315', '#B71C1C','#2E7D32']
}
# Obtener el URL de los tiles
map_id_dict3 = aod_clipped3.getMapId(aod_vis_params)
aod_2010_2013_url = map_id_dict3['tile_fetcher'].url_format

# Cargar la imagen AOD y reclasificarla
aod4 = ee.Image("projects/modern-renderer-413302/assets/AOD_2022")
aod_reclassified4 = aod4.expression(
"b(0) <= 0.08 ? 1 : b(0) <= 0.15 ? 2 : b(0) <= 0.24 ? 3 : b(0) <= 0.3 ? 4 : b(0) <= 0.4 ? 5 : b(0) <= 3 ? 6 : 7"
)

# Cargar la geometría
geometry = ee.FeatureCollection("projects/modern-renderer-413302/assets/ecuador_borde_pol")

# Enmascarar la imagen con la geometría
aod_clipped4 = aod_reclassified4.clipToCollection(geometry)

# Definir los parámetros de visualización
aod_vis_params = {
    'min': 1,
    'max': 7,
    'palette': ['#2E7D32', '#64DD17', '#FFD600', '#FF8C00', '#D84315', '#B71C1C','#2E7D32']
}

# Obtener el URL de los tiles
map_id_dict4 = aod_clipped4.getMapId(aod_vis_params)
aod_2020_2022_url = map_id_dict4['tile_fetcher'].url_format
# Crear el mapa dual
dual_map = DualMap(location=[-0.229, -78.52], zoom_start=12)

# Añadir capas al primer mapa
folium.TileLayer('OpenStreetMap').add_to(dual_map.m1)
folium.TileLayer(
    tiles=lulc_2010_2013_url,
    attr='Google Earth Engine',
    name='LULC 2010-2013'
).add_to(dual_map.m1)
folium.TileLayer(
    tiles=aod_2010_2013_url,
    attr='Google Earth Engine',
    name='AOD 2012'
).add_to(dual_map.m1)

# Añadir capas al segundo mapa
folium.TileLayer('OpenStreetMap').add_to(dual_map.m2)
folium.TileLayer(
    tiles=lulc_2020_2022_url,
    attr='Google Earth Engine',
    name='LULC 2020-2020'
).add_to(dual_map.m2)
folium.TileLayer(
    tiles=aod_2020_2022_url,
    attr='Google Earth Engine',
    name='AOD 2022'
).add_to(dual_map.m2)

# Añadir control de capas a ambos mapas
folium.LayerControl().add_to(dual_map.m1)
folium.LayerControl().add_to(dual_map.m2)

# Ruta de la imagen que quieres agregar
image_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Visualizar_result\mapas\sello-uce-logotipo-universidad-central-ecuador-1-1.png'

# Ruta de la nueva imagen 
image_path_2 = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Visualizar_result\mapas\class.png'

# Ruta de la imagen que se añade dos veces
image_path_3 = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Visualizar_result\mapas\AOD_cat.png'

# Código HTML para añadir ambas imágenes
# Generar el mapa HTML
output_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Visualizar_result\mapas\comparacion_de_mapas_con_imagen_fija.html'
dual_map.save(output_path)

# Código HTML para añadir ambas imágenes
html_images = f"""
    <style>
        #image-overlay {{
            position: absolute;
            top: 5%;
            left: 5%;
            z-index: 9999;
        }}
        #image-overlay-2 {{
            position: absolute;
            top: 30%;
            left: 45%;
            z-index: 9999;
        }}
        #image-overlay-3 {{
            position: absolute;
            top: 80%;
            left: 5%;
            z-index: 9999;
        }}
        #image-overlay-4 {{
            position: absolute;
            top: 80%;
            left: 60%;
            z-index: 9999;
        }}
    </style>
    <div id="image-overlay">
        <img src="file:///{image_path}" width="100" height="auto"/>
    </div>
    <div id="image-overlay-2">
        <img src="file:///{image_path_2}" width="140" height="auto"/>
    </div>
    <div id="image-overlay-3">
        <img src="file:///{image_path_3}" width="480" height="auto"/>
    </div>
    <div id="image-overlay-4">
        <img src="file:///{image_path_3}" width="480" height="auto"/>
    </div>
"""

# Abrir el archivo HTML generado y agregar el código de las imágenes
with open(output_path, 'a') as f:
    f.write(html_images)