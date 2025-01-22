import pandas as pd
import numpy as np
import os
from scipy.stats import zscore

# Define the range for each variable
ranges = {
    'NO2': (0, 100),
    'O3': (0, 85),
    'PM25': (0, 1200),
    'PRE': (200, 780),
    'RS': (0, 1100),
    'SO2': (0, 200),
    'TMP': (7, 28),
    'VEL': (0, 8),
    'CO': (0, 4),
    'DIR': (0, 360),
    'HUM': (60, 90),
    'LLU': (0, 70)
}

# List of input files
archivos = [
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datosproceso_3\Carapungo.csv',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datosproceso_3\Centro.csv',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datosproceso_3\Cotocollao.csv',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datosproceso_3\Belisario.csv',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datosproceso_3\ElCamal.csv',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datosproceso_3\Guamani.csv',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datosproceso_3\LosChillos.csv',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datosproceso_3\SanAntonio.csv',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datosproceso_3\Tumbaco.csv'
]

# Función para realizar el resample de cada archivo
def resample_datos(archivo):
    # Cargar el archivo CSV
    df = pd.read_csv(archivo)
    
    # Convertir la columna 'Fecha' a datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
    
    # Establecer 'Fecha' como índice
    df.set_index('Fecha', inplace=True)
    
    # Convertir todas las columnas a numéricas, excepto 'Fecha'
    for column in df.columns:
        if column != 'Fecha':
            df[column] = pd.to_numeric(df[column], errors='coerce')
    
    # Aplicar el filtro a las columnas según el rango definido
    for column, (min_val, max_val) in ranges.items():
        if column in df.columns:
            df = df[(df[column] >= min_val) & (df[column] <= max_val)]

    # Realizar el resample por frecuencia anual, mensual y semanal
    resampled_annual = df.resample('A').mean()
    resampled_monthly = df.resample('M').mean()
    resampled_weekly = df.resample('W').mean()
    resampled_seasonal = df.resample('Q').mean()
    
    # Definir la ruta de salida para los archivos
    ruta_salida = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datosproceso_3\resample'
    
    # Asegurarse de que la carpeta de salida exista
    os.makedirs(ruta_salida, exist_ok=True)
    
    # Obtener el nombre base del archivo para usarlo en los archivos de salida
    archivo_base = archivo.split("\\")[-1].split('.')[0]

    # Guardar los resultados en archivos separados para cada tipo de resample
    resampled_annual.to_csv(os.path.join(ruta_salida, f'{archivo_base}_Resample_Anual.csv'))
    resampled_monthly.to_csv(os.path.join(ruta_salida, f'{archivo_base}_Resample_Mensual.csv'))
    resampled_weekly.to_csv(os.path.join(ruta_salida, f'{archivo_base}_Resample_Semanal.csv'))
    resampled_seasonal.to_csv(os.path.join(ruta_salida, f'{archivo_base}_Resample_Estacional.csv'))

# Aplicar el resample a los archivos
for archivo in archivos:
    resample_datos(archivo)
