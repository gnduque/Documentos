import geopandas as gpd

# Ruta al archivo GeoJSON original
geojson_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Visualizar_result\mapas\capas\aod_2019_2024.shp'

# Ruta al archivo GeoJSON reproyectado
reprojected_geojson_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Visualizar_result\mapas\capas\aod_2019_2024.geojson'

# Cargar el archivo GeoJSON original
gdf = gpd.read_file(geojson_path)

# Reproyectar a WGS84 (EPSG:4326)
gdf = gdf.to_crs(epsg=4326)

# Guardar el nuevo GeoJSON
gdf.to_file(reprojected_geojson_path, driver="GeoJSON")

print(f"GeoJSON reproyectado guardado en: {reprojected_geojson_path}")
