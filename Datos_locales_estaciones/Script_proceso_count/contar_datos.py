import os
import pandas as pd
import numpy as np
from scipy.stats import zscore

# Ruta de la carpeta que contiene los archivos CSV
folder_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datosproceso_3'

# Lista de archivos específicos que deseas procesar
csv_files = [
    "Carapungo.csv", "SanAntonio.csv", "Tumbaco.csv", "Guamani.csv",
    "Cotocollao.csv", "Belisario.csv", "Centro.csv", "LosChillos.csv", "ElCamal.csv"
]

# Rango de valores permitidos para cada variable
ranges = {
    'NO2': (0, 100),
    'O3': (0, 105),
    'PM25': (0, 300),
    'PRE': (200, 780),
    'RS': (0, 1350),
    'SO2': (0, 200),
    'TMP': (7, 28),
    'VEL': (0, 8),
    'CO': (0, 20),
    'DIR': (0, 360),
    'HUM': (60, 100),
    'LLU': (0, 85)
}

# Variables para almacenar resultados generales
initial_total_rows = 0
initial_total_data = 0
final_total_rows = 0
final_total_data = 0

# Contabilidad individual
file_stats = []
statistical_summaries = []  # Lista para guardar estadísticas descriptivas

# Procesar solo los archivos seleccionados
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    if os.path.exists(file_path):  # Verificar si el archivo existe
        df = pd.read_csv(file_path)  # Leer el archivo CSV

        # Eliminar la columna SO2 solo para Tumbaco.csv
        if file == "Tumbaco.csv" and "SO2" in df.columns:
            df = df.drop(columns=["SO2"])
            print(f"Columna 'SO2' eliminada del archivo {file}")

        # Contar filas y datos iniciales
        initial_rows = len(df)
        initial_data = df.size

        initial_total_rows += initial_rows
        initial_total_data += initial_data

        # Reemplazar valores NaN en la columna AOD con 0
        if 'AOD' in df.columns:
        # Multiplicar la columna AOD por 0.01
            df['AOD'] = df['AOD'] * 0.01
    
        # Luego reemplazar NaN con 0
            df['AOD'] = df['AOD'].fillna(0)

        # Eliminar filas con valores NaN
        df = df.dropna()

        # Eliminar outliers utilizando Z-score
        z_scores = np.abs(zscore(df.select_dtypes(include=[np.number])))
        df = df[(z_scores < 3).all(axis=1)]

        # Eliminar valores fuera de los rangos especificados para cada variable
        for column, (min_val, max_val) in ranges.items():
            if column in df.columns:
                df = df[(df[column] >= min_val) & (df[column] <= max_val)]

        # Calcular rango de fechas después de modificaciones
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')  # Convertir a formato de fecha
            date_min = df['Fecha'].min()
            date_max = df['Fecha'].max()
        else:
            date_min = None
            date_max = None

        # Guardar el archivo modificado
        modified_file_path = os.path.join(folder_path, f"modified_{file}")
        df.to_csv(modified_file_path, index=False)

        # Contar filas y datos después de modificaciones
        final_rows = len(df)
        final_data = df.size

        final_total_rows += final_rows
        final_total_data += final_data

        # Almacenar estadísticas individuales
        file_stats.append({
            'Archivo': file,
            'Filas iniciales': initial_rows,
            'Datos iniciales': initial_data,
            'Filas finales': final_rows,
            'Datos finales': final_data,
            'Fecha inicio': date_min,
            'Fecha fin': date_max
        })

        # Excluir columna Fecha para estadísticas descriptivas
        if 'Fecha' in df.columns:
            df_stats = df.drop(columns=['Fecha'])
        else:
            df_stats = df

        # Calcular estadísticas descriptivas
        stats = df_stats.describe(include='all').transpose()
        stats.insert(0, 'Archivo', file)  # Agregar nombre del archivo
        stats.insert(1, 'Columna', stats.index)  # Agregar nombre de la columna como nueva columna "Columna"
        statistical_summaries.append(stats)

# Crear un DataFrame con los resultados generales
results_df = pd.DataFrame(file_stats)

# Agregar una fila para los totales
totals = {
    'Archivo': 'TOTAL',
    'Filas iniciales': initial_total_rows,
    'Datos iniciales': initial_total_data,
    'Filas finales': final_total_rows,
    'Datos finales': final_total_data,
    'Fecha inicio': None,
    'Fecha fin': None
}
results_df = pd.concat([results_df, pd.DataFrame([totals])], ignore_index=True)

# Guardar el resumen general en un archivo CSV en la nueva ruta especificada
summary_output_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_proceso_count\summary_results.csv"
results_df.to_csv(summary_output_path, index=False)
print(f"\nResumen guardado en: {summary_output_path}")

# Crear un DataFrame para las estadísticas descriptivas y guardarlas en la nueva ruta especificada
stats_summary_df = pd.concat(statistical_summaries, ignore_index=True)
stats_output_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_proceso_count\statistical_summary.csv"
stats_summary_df.to_csv(stats_output_path, index=False)
print(f"\nEstadísticas descriptivas guardadas en: {stats_output_path}")
