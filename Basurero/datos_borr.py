import pandas as pd
import numpy as np
from scipy.stats import zscore

file_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\TMP.xlsx"

# Leer el archivo
df = pd.read_excel(file_path)

# Convertir la columna Fecha a datetime y convertirla a UTC-5
df['Fecha'] = pd.to_datetime(df['Fecha']).dt.tz_localize('UTC').dt.tz_convert('America/Bogota')

# Establecer Fecha como índice
df.set_index('Fecha', inplace=True)

# Convertir las fechas a UTC antes del análisis
df.index = df.index.tz_convert('UTC')

# Filtrar datos desde 2018
df = df[df.index >= '2018-01-01']

# Procesar cada estación por separado
for col in df.columns:
    # Copiar los datos de la estación para procesarlos individualmente
    station_data = df[[col]].dropna()
    initial_count = len(station_data)
    
    # Filtrar los valores fuera del rango 0-300
    out_of_range = station_data[~station_data[col].between(0, 300, inclusive='both')]
    station_data = station_data[station_data[col].between(0, 300, inclusive='both')]
    range_filtered_count = initial_count - len(station_data)
    
    # Eliminar outliers usando Z-score
    z_scores = np.abs(zscore(station_data[col].dropna()))
    z_outliers = station_data[z_scores >= 3]
    station_data = station_data[z_scores < 3]
    z_filtered_count = len(z_outliers)

    # Guardar detalles de datos eliminados
    removed_data = pd.concat([out_of_range, z_outliers])
    output_file = f"C:\\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Basurero\\{col}_TMP_removed_data.csv"
    removed_data.to_csv(output_file)

    print(f"Estación: {col}")
    print(f"Datos eliminados por rango (0-300): {range_filtered_count}")
    print(f"Datos eliminados por Z-score: {z_filtered_count}")
    print(f"Archivo con datos eliminados guardado en: {output_file}")
