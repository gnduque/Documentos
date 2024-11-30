import pandas as pd
import numpy as np
import os
from scipy.stats import zscore

# Lista de archivos a procesar
files = [
    "Max_Belisario.csv", "Max_Carapungo.csv", "Max_Centro.csv", 
    "Max_Cotocollao.csv", "Max_ElCamal.csv", "Max_Guamani.csv", 
    "Max_LosChillos.csv", "Max_SanAntonio.csv", "Max_Tumbaco.csv"
]

# Directorio donde se encuentran los archivos
data_dir = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datosproceso_3'

# Rango de valores para las columnas
ranges = {
    'NO2': (0, 100),
    'O3': (0, 85),
    'PM25': (0, 300),
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

# Operaciones para obtener el máximo
default_operations = {
    'NO2': 'max',
    'O3': 'max',
    'PM25': 'max',
    'PRE': 'max',
    'RS': 'max',
    'SO2': 'max',
    'TMP': 'max',
    'VEL': 'max',
    'CO': 'max',
    'DIR': 'max',
    'HUM': 'max',
    'LLU': 'max',
    'AOD': 'max'
}

san_antonio_operations = default_operations.copy()
for col in ['CO', 'NO2']:
    san_antonio_operations.pop(col, None)

tumbaco_operations = default_operations.copy()
tumbaco_operations.pop('SO2', None)

# Lista para almacenar los resultados de las correlaciones AOD
correlation_results = []

# Procesar cada archivo
for file in files:
    filepath = os.path.join(data_dir, file)
    
    try:
        # Cargar datos
        data = pd.read_csv(filepath)

        # Convertir 'Fecha' a datetime y usarla como índice
        data['Fecha'] = pd.to_datetime(data['Fecha'])
        data.set_index('Fecha', inplace=True)

        # Eliminar columnas específicas solo si existen
        if 'SanAntonio' in file:
            data = data.drop(columns=['CO', 'NO2'], errors='ignore')
        elif 'Tumbaco' in file:
            data = data.drop(columns=['SO2'], errors='ignore')

        # Reemplazar NaN en la columna AOD por 0
        data['AOD'] = data['AOD'].fillna(0)

        # Eliminar filas con NaN en las demás columnas
        data = data.dropna()

        # Filtrar según los rangos
        for column, (min_val, max_val) in ranges.items():
            if column in data.columns:
                data = data[(data[column] >= min_val) & (data[column] <= max_val)]

        # Eliminar outliers utilizando Z-score
        z_scores = np.abs(zscore(data.select_dtypes(include=[np.number])))
        data = data[(z_scores < 3).all(axis=1)]

        # Determinar las operaciones según la estación
        if 'SanAntonio' in file:
            operations = san_antonio_operations
        elif 'Tumbaco' in file:
            operations = tumbaco_operations
        else:
            operations = default_operations

        # Resampling anual con la operación max
        data_resampled = data.resample('A').agg(operations)

        # Calcular la correlación de Pearson
        correlation = data_resampled.corr(method='pearson')

        # Extraer las correlaciones de AOD
        if 'AOD' in correlation.columns:
            aod_correlation = correlation['AOD'].drop('AOD', errors='ignore')
            correlation_results.append(aod_correlation.rename(file.replace(".csv", "")))

    except FileNotFoundError:
        print(f"File not found: {file}")
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Combinar todas las correlaciones AOD en un solo DataFrame
if correlation_results:
    aod_correlation_table = pd.concat(correlation_results, axis=1)
    
    # Guardar los resultados en un archivo CSV en el directorio de resultados
    output_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Resultados_correlaciones\AOD_Correlations_Max_Annual.csv'
    aod_correlation_table.to_csv(output_path)

    # Mostrar la tabla combinada de correlaciones
    print(aod_correlation_table)
else:
    print("No se encontraron correlaciones de AOD para procesar.")
