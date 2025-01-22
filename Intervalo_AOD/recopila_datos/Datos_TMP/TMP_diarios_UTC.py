import pandas as pd
import numpy as np
from scipy.stats import zscore
import pytz

# Cargar el DataFrame desde el archivo CSV
df = pd.read_csv(r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_TMP\TMP.csv")

if df.empty:
    print("El archivo no contiene datos.")
else:
    print("Archivo cargado correctamente.")
    print(df.head())

processed_data = []

# Convertir la columna 'Fecha' a datetime y ajustar de UTC-5 a UTC
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d %H:%M:%S')
local_timezone = pytz.timezone('Etc/GMT+5')  # UTC-5
utc_timezone = pytz.utc
df['Fecha'] = df['Fecha'].dt.tz_localize(local_timezone).dt.tz_convert(utc_timezone)

for col in df.columns[1:]:  # Ignorar la columna 'Fecha'
    print(f"Procesando datos para la estación: {col}")
    station_data = pd.to_numeric(df[col], errors='coerce').dropna()
    station_data = station_data[station_data.between(-50, 50, inclusive='both')]
    z_scores = np.abs(zscore(station_data))
    station_data = station_data[z_scores < 3]

    if not station_data.empty:
        print(f"Datos válidos para {col}: {len(station_data)} registros.")
        # Asignar el índice basado en 'Fecha' para la estación
        station_data.index = df.loc[station_data.index, 'Fecha']

        # Verificar que el índice sea un DatetimeIndex
        if not isinstance(station_data.index, pd.DatetimeIndex):
            station_data.index = pd.to_datetime(station_data.index)

        # Resamplear a diario
        station_resampled = station_data.resample('D').mean()
        station_resampled = station_resampled.to_frame(name=col)
        processed_data.append(station_resampled)
    else:
        print(f"No hay datos válidos para la estación {col} después del procesamiento.")

if processed_data:
    final_df = pd.concat(processed_data, axis=1)
    output_file = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_TMP\TMP_daily_all_stations.csv"
    final_df.to_csv(output_file)
    print(f"Archivo procesado guardado en {output_file}")
else:
    print("No hay datos procesados para guardar.")
    
