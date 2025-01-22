import geopandas as gpd
from tqdm import tqdm
import time

# Ruta del archivo shapefile de entrada
shapefile_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Visualizar_result\mapas\capas\aod_2009_2015.shp'

# Ruta de salida para el archivo GeoJSON
geojson_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Visualizar_result\mapas\capas\aod_2009_2015.geojson'

# Cargar el shapefile
print("Cargando shapefile...")
gdf = gpd.read_file(shapefile_path)

# Simular barra de progreso para la conversión
print("Convirtiendo a GeoJSON...")
for _ in tqdm(range(100), desc="Progreso"):
    time.sleep(0.02)  # Simulación del proceso de conversión

# Guardar el GeoJSON
gdf.to_file(geojson_path, driver="GeoJSON")
print(f"GeoJSON guardado en: {geojson_path}")
