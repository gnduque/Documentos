import rasterio
from rasterio.enums import ColorInterp

# Ruta del archivo raster original y salida
raster_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Clasifica_RF_CART_SVM\Raster_Results\LULC_2010_2014_RF.tif"
output_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Clasifica_RF_CART_SVM\Raster_Results\LULC_2010_2014_RF_colored.tif"

# Valores de píxel y colores hexadecimales
pixel_values = [1, 2, 3, 7, 8, 9, 10, 11, 12, 13]
hex_colors = ['#AEC3D4', '#132007', '#90ae41', '#00FFFF', '#fdf6f2', '#683401', '#CC0013', '#6F6F6F', '#ffff00', '#CDB33B']

# Convertir colores hexadecimales a RGB
def hex_to_rgb(hex_color):
    return tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

# Crear la tabla de colores (dict: {pixel_value: (R, G, B)})
color_table = {value: hex_to_rgb(color) for value, color in zip(pixel_values, hex_colors)}

# Leer el raster original
with rasterio.open(raster_path) as src:
    raster_data = src.read(1)  # Leer la primera banda
    profile = src.profile

# Actualizar el perfil del raster para incluir una sola banda
profile.update(count=1, dtype='uint8', photometric='palette')

# Guardar el nuevo raster con la tabla de colores
with rasterio.open(output_path, 'w', **profile) as dst:
    dst.write(raster_data, 1)  # Escribir la banda única
    dst.write_colormap(1, color_table)  # Asignar la tabla de colores
