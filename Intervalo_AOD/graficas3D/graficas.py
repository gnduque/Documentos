import numpy as np
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from matplotlib import cm as plt_cm

# Cargar el shapefile
gdf = gpd.read_file(r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\graficas3D\borde_quito.shp")

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

# Intervalos de fechas
intervalos_fechas = [
    ('12/1/2018', '2/28/2019'),
    ('3/1/2019', '5/31/2019'),
    ('6/1/2019', '8/31/2019'),
    ('9/1/2019', '11/30/2019'),
    ('12/1/2019', '2/29/2020'),
    ('3/1/2020', '5/31/2020'),
    ('6/1/2020', '8/31/2020'),
    ('9/1/2020', '11/30/2020'),
    ('12/1/2020', '2/28/2021'),
    ('3/1/2021', '5/31/2021'),
    ('6/1/2021', '8/31/2021'),
    ('9/1/2021', '11/30/2021'),
    ('12/1/2023', '2/29/2024'),
    ('3/1/2024', '5/31/2024'),
    ('6/1/2024', '8/31/2024'),
    ('9/1/2024', '11/30/2024'),
]

# Para cada intervalo de fechas
for inicio, fin in intervalos_fechas:
    pm25_values = []
    aod_values = []

    # Filtrar y calcular para cada estación
    for estacion in archivos_estaciones:
        archivo_estacion = archivos_estaciones[estacion]
        df = pd.read_csv(archivo_estacion, parse_dates=['Fecha'], dayfirst=False)
        df_filtrado = df[(df['Fecha'] >= inicio) & (df['Fecha'] <= fin)]
        
        # Media de PM25
        pm25_media = df_filtrado['PM25'].dropna().mean()
        pm25_values.append(pm25_media)
        
        # Media de AOD
        aod_media = df_filtrado['AOD_media'].dropna().mean()
        aod_values.append(aod_media)

    # Crear una nueva figura para cada intervalo
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Graficar las barras 3D
    dx = dy = 0.01
    cmap_aod = plt_cm.get_cmap('RdYlGn_r')
    norm = Normalize(vmin=50, vmax=100)
    colors_aod = [cmap_aod(norm(aod)) for aod in aod_values]
    cmap = plt.cm.get_cmap('Set1', len(pm25_values))
    colors_borders = [cmap(i) for i in range(len(pm25_values))]

    for i, (lat, lon, nombre) in enumerate(zip(latitudes, longitudes, nombres_estaciones)):
        bar = ax.bar3d(lon - dx / 2, lat - dy / 2, 0, dx, dy, pm25_values[i], color=colors_aod[i], edgecolor=colors_borders[i])
        ax.text(lon, lat, pm25_values[i] + 0.15, f'{pm25_values[i]:.2f}', color='black', fontsize=8, ha='center')

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

    plt.title(f'Gráfica de PM25 y AOD: {inicio} - {fin}')
    plt.show()
