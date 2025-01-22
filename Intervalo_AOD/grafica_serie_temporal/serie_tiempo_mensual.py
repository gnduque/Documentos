import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.stats import zscore

# Función para cargar, limpiar y resamplear los datos
def load_clean_and_resample(filepath, date_range, variables_to_keep, value_replacement, ranges):
    if not os.path.exists(filepath):
        print(f"Error: El archivo {filepath} no existe.")
        return None

    data = pd.read_csv(filepath, parse_dates=['Fecha'])
    data.columns = [col.strip() for col in data.columns]  # Eliminar espacios
    data = data[(data['Fecha'] >= date_range[0]) & (data['Fecha'] <= date_range[1])]
    data = data[variables_to_keep]
    data['AOD'] = data['AOD'].fillna(value_replacement)
    data = data.dropna()
    
    # Filtrar los datos según los rangos antes de hacer el resampleo
    for col, (lower, upper) in ranges.items():
        data = data[(data[col] >= lower) & (data[col] <= upper)]
    
    # Aplicar filtro de outliers usando Z-score antes del resampleo
    z_scores = np.abs(zscore(data.select_dtypes(include=[np.number])))
    data = data[(z_scores < 3).all(axis=1)]  # Eliminar filas con Z-score > 3 (outliers)
    
    # Resampleo mensual: PM25 y AOD con promedio
    data.set_index('Fecha', inplace=True)
    resampled_data = data.resample('M').agg({'AOD': 'mean', 'PM25': 'mean'}).reset_index()

    # Normalización Min-Max para PM25 y AOD
    resampled_data['PM25_normalized'] = (resampled_data['PM25'] - resampled_data['PM25'].min()) / (resampled_data['PM25'].max() - resampled_data['PM25'].min())
    resampled_data['AOD_normalized'] = (resampled_data['AOD'] - resampled_data['AOD'].min()) / (resampled_data['AOD'].max() - resampled_data['AOD'].min())
    
    return resampled_data

# Parámetros
filepaths = [
    "C:\\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Datos_locales_estaciones\\Datosproceso_3\\Cotocollao.csv",
    "C:\\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Datos_locales_estaciones\\Datosproceso_3\\Belisario.csv",
    "C:\\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Datos_locales_estaciones\\Datosproceso_3\\Carapungo.csv",
    "C:\\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Datos_locales_estaciones\\Datosproceso_3\\Centro.csv",
    "C:\\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Datos_locales_estaciones\\Datosproceso_3\\Guamani.csv",
    "C:\\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Datos_locales_estaciones\\Datosproceso_3\\LosChillos.csv",
    "C:\\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Datos_locales_estaciones\\Datosproceso_3\\SanAntonio.csv",
    "C:\\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Datos_locales_estaciones\\Datosproceso_3\\Tumbaco.csv",
    "C:\\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Datos_locales_estaciones\\Datosproceso_3\\ElCamal.csv"
]
date_range = ("2016-02-08", "2024-02-13")
variables_to_keep = ['Fecha', 'AOD', 'PM25']
value_replacement = 0
ranges = {'PM25': (0, 300)}  # Filtro antes del resampleo

# Crear la figura y los subgráficos
fig, axes = plt.subplots(3, 3, figsize=(9, 9))  # Tamaño más pequeño para gráficos compactos
axes = axes.flatten()

# Procesar cada archivo y graficar
for i, filepath in enumerate(filepaths):
    station_name = filepath.split("\\")[-1].replace(".csv", "")
    data = load_clean_and_resample(filepath, date_range, variables_to_keep, value_replacement, ranges)
    if data is not None and not data.empty:
        # Crear un gráfico para PM25 y AOD con dos ejes Y
        ax1 = axes[i]
        ax2 = ax1.twinx()  # Crear el segundo eje y para AOD
        
        # Graficar PM25 normalizado (promedio) en el eje y izquierdo
        ax1.plot(data['Fecha'], data['PM25_normalized'], color='green', label='PM25 (Normalizado)', linestyle='-', linewidth=1)
        ax1.set_ylabel("PM25", fontsize=8, labelpad=2, color='green')
        ax1.tick_params(axis='y', labelsize=8, labelcolor='green')

        # Graficar AOD normalizado (media) en el eje y derecho
        ax2.plot(data['Fecha'], data['AOD_normalized'], color='blue', label='AOD (Normalizado)', linestyle='-', linewidth=1)
        ax2.set_ylabel("AOD", fontsize=8, labelpad=2, color='blue')
        ax2.tick_params(axis='y', labelsize=8, labelcolor='blue')
        
        # Ajustar los valores del eje X (fechas con formato yyyy/mm) y cada 6 meses
        ax1.set_xticks(data['Fecha'][::6])  # Selecciona un tick cada 6 meses
        ax1.set_xticklabels(data['Fecha'][::6].dt.strftime('%Y/%m'), rotation=90, fontsize=5)  # Formato yyyy/mm, rotación vertical

        # Título y ajustes del gráfico
        ax1.set_title(station_name, fontsize=9)
        ax1.tick_params(axis='x', labelsize=5)

        # Añadir leyenda para las dos series
        ax1.legend(loc='upper left', fontsize=7)
        ax2.legend(loc='upper right', fontsize=7)

    else:
        axes[i].set_visible(False)

# Ajustar diseño y mostrar la figura
plt.tight_layout()
plt.show()
