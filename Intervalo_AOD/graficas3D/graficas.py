import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D

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

fig = plt.figure(figsize=(50, 10))  # Cambié el tamaño de la figura para hacerla más grande
ax = fig.add_subplot(111, projection='3d')

latitudes = estaciones_df['latitud']
longitudes = estaciones_df['longitud']
nombres_estaciones = estaciones_df['nombre']

pm25_values = []
aod_values = []
tmp_values = []

# Calcular la media de PM25, AOD y TMP para cada estación en el rango de fechas
for estacion in archivos_estaciones:
    archivo_estacion = archivos_estaciones[estacion]
    df = pd.read_csv(archivo_estacion, parse_dates=['Fecha'], dayfirst=False)
    
    #Escalar el valor de AOD
    df['AOD_mean'] = df['AOD_mean'] * 0.001

    # Filtrar datos para el rango de fechas 
    df_filtrado = df[(df['Fecha'] >= '2024-09-26') & (df['Fecha'] <= '2024-09-26')]
    
    # Media de PM25
    pm25_media = df_filtrado['PM25'].dropna().mean()
    pm25_values.append(pm25_media)
    
    # Media de AOD
    AOD_mean = df_filtrado['AOD_mean'].dropna().mean()
    aod_values.append(AOD_mean)
    
    # Media de TMP
    tmp_media = df_filtrado['TMP'].dropna().mean()
    tmp_values.append(tmp_media)
    
    print(f"Estación: {estacion}, Media PM25: {pm25_media}, Media AOD: {AOD_mean}, Media TMP: {tmp_media}")  # Verificar valores

dx = dy = 0.01
dz = pm25_values

# Definir los colores según los intervalos de AOD proporcionados
def get_aod_color(aod):
    if np.isnan(aod):
        return '#00000000'  # Transparente (RGBA con alpha=0)
    elif 0 <= aod < 0.300:
        return '#0000ff'
    elif 0.300 <= aod < 0.400:
        return '#800080'
    elif 0.400 <= aod < 0.600:
        return '#00ffff'
    else:
        return '#ffff00'

colors_aod = [get_aod_color(aod) for aod in aod_values]

# Colormap para los bordes (colores de las estaciones)
cmap = plt.cm.get_cmap('Set1', len(pm25_values))
colors_borders = [cmap(i) for i in range(len(pm25_values))]

handles = []

# Graficar las barras 3D
for i, (lat, lon, nombre) in enumerate(zip(latitudes, longitudes, nombres_estaciones)):
    if np.isnan(pm25_values[i]):
        # Configuración para NaN en PM2.5
        bar_height = 20  # Altura fija
        bar_color = colors_aod[i]  # Color según AOD
        bar_edgecolor = 'none'  # Sin borde
    else:
        # Configuración para valores válidos
        bar_height = pm25_values[i]
        bar_color = colors_aod[i]
        bar_edgecolor = colors_borders[i]  # Borde de la estación correspondiente
    
    # Graficar la barra
    ax.bar3d(lon - dx / 2, lat - dy / 2, 0, dx, dy, bar_height, color=bar_color, edgecolor=bar_edgecolor)
    
    # Colocar texto PM25 sobre cada barra en azul
    ax.text(lon-0.01, lat, dz[i] + 1.5, f'{dz[i]:.1f}', color='blue', fontsize=6, ha='center', va='bottom', rotation=180)

    handle = Line2D([0], [0], marker='o', color='w', markerfacecolor=colors_borders[i], markersize=10, label=nombre)
    handles.append(handle)

# Leyenda para AOD con los colores especificados
aod_legend_labels = [
    '[0 - 0.300) Deseable',
    '[0.300 - 0.400 Aceptable)',
    '[0.400 - 0.600) Precaución',
    '>= 0.600 Superior'
]
aod_legend_colors = [
    '#0000ff',
    '#800080',
    '#00ffff',
    '#ffff00'
]
aod_handles = [Line2D([0], [1], color=color, lw=4, label=label) for label, color in zip(aod_legend_labels, aod_legend_colors)]

# Configuración de los ejes
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')
ax.set_zlabel('PM2.5 (μg/m³)', color='blue', labelpad=-5)  # Título del eje Z en azul
ax.set_zlim(0, 30)  # Limitar el eje Z hasta 30
ax.set_zticks(np.arange(0, 31, 5))  # Establecer ticks de 5 en 5 hasta 30
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
ax.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, -0.04), ncol=3)

# Leyenda para AOD a la derecha
fig.legend(handles=aod_handles, loc='center left', bbox_to_anchor=(0.8, 0.5), title='AOD')

# Ajustar la distancia entre los valores y el eje Z
# Ajustar la distancia entre los valores y los ejes X, Y y Z
ax.tick_params(axis='x', pad=1)  # Ajustar el padding para los ticks del eje X
ax.tick_params(axis='y', pad=-4)  # Ajustar el padding para los ticks del eje Y
ax.tick_params(axis='z', pad=-1)  # Ajustar el padding para los ticks del eje Z
plt.subplots_adjust(top=0.85, bottom=0.25, right=0.85)  # Ajustar la posición de la gráfica

plt.show()