import ee

# Inicializar Google Earth Engine
ee.Initialize(project='modern-renderer-413302')


# Configuración inicial
geometria = ee.FeatureCollection("projects/modern-renderer-413302/assets/ecuador_borde_pol")  # Reemplaza con tu geometría
banda = 'Optical_Depth_047'
titulo = 'AOD'
umbral_filtro = 50000

# 1. Importar colección
coleccion = (ee.ImageCollection('MODIS/061/MCD19A2_GRANULES')
             .select(banda)
             .filterBounds(geometria))

# Obtener la resolución espacial
resolucion_espacial = ee.Image(coleccion.first()).select(banda).projection().nominalScale().getInfo()

# Escalar los valores de la banda
coleccion_escala = coleccion.map(lambda img: img.multiply(1).copyProperties(img, ['system:time_start']))

# Función para filtrar y calcular la media
def filtrar_y_calcular_media(coleccion, fecha_inicio, fecha_fin, geometria, umbral):
    imagenes = (coleccion.filterDate(fecha_inicio, fecha_fin)
                .map(lambda img: img.updateMask(img.lte(umbral))))
    media = ee.Image(imagenes.mean()).clip(geometria)
    return media

# Fechas de análisis
rango_fechas = {
    "lluvioso": ("2013-01-01", "2013-03-31"),
    "trans_seco": ("2013-04-01", "2013-06-30"),
    "seco": ("2013-07-01", "2013-09-30"),
    "trans_lluvia": ("2013-10-01", "2013-12-31"),
    "lluvioso1": ("2021-01-01", "2021-03-31"),
    "trans_seco1": ("2021-04-01", "2021-06-30"),
    "seco1": ("2021-07-01", "2021-09-30"),
    "trans_lluvia1": ("2021-10-01", "2021-12-31")
}

# Procesar imágenes para cada rango de fechas
imagenes = {}
for clave, (fecha_inicio, fecha_fin) in rango_fechas.items():
    imagen = filtrar_y_calcular_media(coleccion_escala, fecha_inicio, fecha_fin, geometria, umbral_filtro)
    imagenes[clave] = imagen

# Exportar imágenes a Google Drive
def exportar_imagen(imagen, nombre, geometria, escala):
    tarea = ee.batch.Export.image.toDrive(
        image=imagen,
        description=nombre,
        folder='AOD',
        region=geometria.geometry().bounds().getInfo()['coordinates'],
        scale=30,
        crs='EPSG:32717',
        maxPixels=1e10
    )
    tarea.start()
    print(f"Exportación iniciada: {nombre}")

# Exportar cada imagen
for clave, imagen in imagenes.items():
    nombre = f"AOD_{rango_fechas[clave][0]}_{rango_fechas[clave][1]}"
    exportar_imagen(imagen, nombre, geometria, resolucion_espacial)

print("Exportación completa. Revisa tu Google Drive.")
