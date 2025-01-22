import geopandas as gpd
import pandas as pd  # Se agrega esta línea para importar pandas

# Cargar los shapefiles
shp1_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Rasteriza_lul_igm\vacio_raster.shp"
shp2_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Rasteriza_lul_igm\lulc_actualizado.shp"

shp1 = gpd.read_file(shp1_path)
shp2 = gpd.read_file(shp2_path)

# Unir los shapefiles
shp_union = gpd.GeoDataFrame(pd.concat([shp1, shp2], ignore_index=True))

# Guardar la unión en un nuevo archivo
output_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Rasteriza_lul_igm\union_resultante.shp"
shp_union.to_file(output_path)

print(f"Archivo combinado guardado en: {output_path}")
