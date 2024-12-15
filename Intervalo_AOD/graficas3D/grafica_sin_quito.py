import numpy as np
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from matplotlib import cm as plt_cm

# Cargar el shapefile
gdf = gpd.read_file(r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_periodos\borde_quito.shp")

# Cargar los datos de estaciones
estaciones_df = pd.read_csv(r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\graficas3D\ubi_estaciones.csv")

# Extraer las columnas necesarias
latitudes = estaciones_df['latitud'].values
longitudes = estaciones_df['longitud'].values
nombres_estaciones = estaciones_df['nombre'].values

archivos_estaciones = {
    'Carapungo': r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\graficas3D\Carapungo.csv",
    'SanAntonio': r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\graficas3D\SanAntonio.csv",
    'Tumbaco': r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\graficas3D\Tumbaco.csv",
    'Guamani': r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\graficas3D\Guamani.csv",
    'Cotocollao': r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\graficas3D\Cotocollao.csv",
    'Belisario': r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\graficas3D\Belisario.csv",
    'Centro': r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\graficas3D\Centro.csv",
    'LosChillos': r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\graficas3D\LosChillos.csv",
    'ElCamal': r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\graficas3D\ElCamal.csv"
}

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Graficar cada polígono
for _, row in gdf.iterrows():
    x, y = row['geometry'].exterior.xy
    z = [0] * len(x)
    ax.plot(x, y, z, color='b')

latitudes = estaciones_df['latitud']
longitudes = estaciones_df['longitud']
nombres_estaciones = estaciones_df['nombre']

pm25_values = []
aod_values = []

# Calcular la media de PM25 y AOD para cada estación en el rango de fechas
for estacion in archivos_estaciones:
    archivo_estacion = archivos_estaciones[estacion]
    df = pd.read_csv(archivo_estacion, parse_dates=['Fecha'], dayfirst=False)
    df_filtrado = df[(df['Fecha'] >= '12/1/2018') & (df['Fecha'] <= '2/28/2024')]
    
    # Media de PM25
    pm25_media = df_filtrado['PM25'].dropna().mean()
    pm25_values.append(pm25_media)
    
    # Media de AOD
    aod_media = df_filtrado['AOD_media'].dropna().mean()
    aod_values.append(aod_media)
    
    print(f"Estación: {estacion}, Media PM25: {pm25_media}, Media AOD: {aod_media}")  # Verificar valores

dx = dy = 0.01
dz = pm25_values

# Colormap para los colores de AOD (invertido: 100 a 50, rojo a verde)
cmap_aod = plt_cm.get_cmap('RdYlGn_r')  # Colormap invertido (rojo a verde)
norm = Normalize(vmin=50, vmax=100)  # Normalización de 50 (rojo) a 100 (verde)
colors_aod = [cmap_aod(norm(aod)) for aod in aod_values]

# Colormap para los bordes (colores de las estaciones)
cmap = plt.cm.get_cmap('Set1', len(pm25_values))
colors_borders = [cmap(i) for i in range(len(pm25_values))]

handles = []

# Graficar las barras 3D
for i, (lat, lon, nombre) in enumerate(zip(latitudes, longitudes, nombres_estaciones)):
    bar = ax.bar3d(lon - dx / 2, lat - dy / 2, 0, dx, dy, dz[i], color=colors_aod[i], edgecolor=colors_borders[i])  # Relleno según AOD y borde según estación
    ax.text(lon, lat, dz[i] + 0.15, f'{dz[i]:.2f}', color='black', fontsize=8, ha='center')  # Ajustar altura del texto para PM25

    handle = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors_borders[i], markersize=10, label=nombre)
    handles.append(handle)

# Leyenda para AOD
sm = plt.cm.ScalarMappable(cmap=cmap_aod, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, orientation='vertical', pad=0.1)
cbar.set_label('AOD', rotation=270, labelpad=15)  # Etiqueta de la leyenda actualizada

# Configuración de los ejes
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')
ax.set_zlabel('PM2.5 (μg/m³)')  # Nombre del eje Z actualizado
ax.set_zlim(0, max(pm25_values))
ax.view_init(elev=30, azim=200)
ax.set_xlim(-78.58, -78.37)
ax.set_ylim(-0.35, 0.00)
ax.set_xticks(np.arange(-78.58, -78.37, 0.05)[1:-1])
ax.set_yticks(np.arange(-0.35, 0.01, 0.05)[1:-1])
for tick in ax.get_xticklabels():
    tick.set_rotation(-20)
for tick in ax.get_yticklabels():
    tick.set_rotation(45)
for tick in ax.get_xticklabels() + ax.get_yticklabels():
    tick.set_fontsize(8)

# Leyenda para los colores de los bordes
ax.legend(handles=handles, loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=3)

plt.show()
