import folium
from folium import GeoJson
import json

geojson_file = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Visualizar_result\mapas\capas\aod_2009_2015.geojson'

try:
    with open(geojson_file, 'r') as f:
        geojson_data = json.load(f)
    print("GeoJSON cargado correctamente.")
except Exception as e:
    print(f"Error al cargar el archivo GeoJSON: {e}")

if geojson_data:
    m = folium.Map(location=[-0.229, -78.52], zoom_start=10)

    geojson_layer = GeoJson(
        geojson_data,
        tooltip=folium.GeoJsonTooltip(
            fields=['VALUE'],
            aliases=['Valor:'],
            localize=True,
            labels=True,
            sticky=False,
            parse_html=True,
            default=None
        ),
        style_function=lambda x: {
            'fillColor': 'transparent',
            'color': 'transparent',
            'weight': 0
        }
    )

    geojson_layer.add_to(m)

    output_file = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Visualizar_result\mapas\aod_map.html'
    m.save(output_file)
    print(f"Mapa guardado correctamente en {output_file}")
else:
    print("No se cargaron los datos GeoJSON correctamente.")
