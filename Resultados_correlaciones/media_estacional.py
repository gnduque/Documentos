import pandas as pd
import numpy as np
import os

# Path to the data directory
data_dir = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datosproceso_3'

# List of files to process
stations = [
    "modified_Carapungo.csv", "modified_SanAntonio.csv", "modified_Tumbaco.csv",
    "modified_Guamani.csv", "modified_Cotocollao.csv", "modified_Belisario.csv",
    "modified_Centro.csv", "modified_LosChillos.csv", "modified_ElCamal.csv"
]

# Updated ranges
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

# Updated operations
default_operations = {
    'NO2': 'mean',
    'O3': 'mean',
    'PM25': 'mean',
    'PRE': 'mean',
    'RS': 'mean',
    'SO2': 'mean',
    'TMP': 'mean',
    'VEL': 'mean',
    'CO': 'mean',
    'DIR': 'mean',
    'HUM': 'mean',
    'LLU': 'mean',
    'AOD': 'mean'
}

san_antonio_operations = default_operations.copy()
for col in ['CO', 'NO2']:
    san_antonio_operations.pop(col, None)

tumbaco_operations = default_operations.copy()
tumbaco_operations.pop('SO2', None)

# Period definitions (4 periods within a year)
periods = [('11-16', '02-15'), ('02-16', '05-15'), ('05-16', '08-15'), ('08-16', '11-15')]
period_labels = ['16Nov-15Feb', '16Feb-15May', '16May-15Aug', '16Aug-15Nov']

# Prepare a list to hold the period data for each station
correlation_results = []

# Process each station
for station in stations:
    # Construct file path
    filepath = os.path.join(data_dir, station)
    
    try:
        # Load data
        data = pd.read_csv(filepath)

        # Convert 'Fecha' to datetime and set as index
        data['Fecha'] = pd.to_datetime(data['Fecha'])
        data.set_index('Fecha', inplace=True)

        # Eliminar columnas específicas solo si existen
        if 'SanAntonio' in station:
            data = data.drop(columns=['CO', 'NO2'], errors='ignore')
            operations = san_antonio_operations
        elif 'Tumbaco' in station:
            data = data.drop(columns=['SO2'], errors='ignore')
            operations = tumbaco_operations
        else:
            operations = default_operations

        # Filter based on ranges
        for column, (min_val, max_val) in ranges.items():
            if column in data.columns:
                data = data[(data[column] >= min_val) & (data[column] <= max_val)]

        # Lista para guardar los DataFrames de cada periodo
        data_frames = []

        # Iterar sobre cada año desde 2004 hasta 2024
        for year in range(2004, 2025):
            for (start_suffix, end_suffix), label in zip(periods, period_labels):
                start = f"{year}-{start_suffix}"
                end = f"{year}-{end_suffix}" if start_suffix < end_suffix else f"{year+1}-{end_suffix}"
                period_range = data[start:end]
                if not period_range.empty:
                    # Realizamos el re-muestreo según las operaciones definidas
                    period_data = period_range.agg(operations)
                    period_data.name = f"{label} {year}"
                    data_frames.append(period_data.to_frame().transpose())

        # Concatenamos todos los DataFrames en uno solo
        station_data = pd.concat(data_frames)

        # Calculate Pearson correlation for each period
        correlation = station_data.corr(method='pearson')

        # Extract AOD correlations and append to results
        if 'AOD' in correlation.columns:
            aod_correlation = correlation['AOD'].drop('AOD', errors='ignore')
            correlation_results.append(aod_correlation.rename(station.replace(".csv", "")))

    except FileNotFoundError:
        print(f"File not found: {station}")
    except Exception as e:
        print(f"Error processing {station}: {e}")

# Combine all AOD correlations into a single DataFrame
if correlation_results:
    aod_correlation_table = pd.concat(correlation_results, axis=1)

    # Save the results to a CSV in the specified path with the added description
    output_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Resultados_correlaciones\AOD_Correlations_Periods_Mean.csv'
    aod_correlation_table.to_csv(output_path)

    # Display the combined correlation table
    print(aod_correlation_table)
else:
    print("No se encontraron correlaciones de AOD para procesar.")
