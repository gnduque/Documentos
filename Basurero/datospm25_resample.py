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

# Convertir las fechas a UTC antes del resampleo
df.index = df.index.tz_convert('UTC')

# Procesar cada estación por separado
for col in df.columns:
    # Copiar los datos de la estación para procesarlos individualmente
    station_data = df[[col]].dropna()
    
    # Filtrar los valores fuera del rango 1-28
    station_data = station_data[station_data[col].between(1, 28, inclusive='both')]
    
    # Eliminar outliers usando Z-score
    z_scores = np.abs(zscore(station_data[col].dropna()))
    station_data = station_data[z_scores < 3]
    
    # Resamplear a diario y calcular la media
    station_resampled = station_data.resample('D').mean()

    # Guardar el archivo CSV para la estación
    output_file = f"C:\\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Basurero\\{col}_TMP_daily.csv"
    station_resampled.to_csv(output_file)

    print(f"Archivo procesado guardado para la estación {col} en {output_file}")
