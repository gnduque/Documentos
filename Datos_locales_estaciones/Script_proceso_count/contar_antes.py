import os
import pandas as pd

# Ruta de la carpeta que contiene los archivos CSV
folder_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datosproceso_3'

# Lista de archivos específicos que deseas procesar
csv_files = [
    "Carapungo.csv", "SanAntonio.csv", "Tumbaco.csv", "Guamani.csv",
    "Cotocollao.csv", "Belisario.csv", "Centro.csv", "LosChillos.csv", "ElCamal.csv"
]

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

        # Convertir todas las columnas excepto 'Fecha' a numéricas
        columns_to_convert = [col for col in df.columns if col != 'Fecha']
        df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric, errors='coerce')

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
            df['AOD'] = df['AOD'] * 0.001  # Multiplicar la columna AOD por 0.01
           # df['AOD'] = df['AOD'].fillna(0)  # Reemplazar NaN con 0

        # Convertir la columna Fecha a formato datetime y filtrar por rango de fechas
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')  # Convertir a datetime
            df = df[(df['Fecha'] >= '2019-01-01') & (df['Fecha'] <= '2021-12-31')]  # Filtrar por rango de fechas
            df = df.dropna(subset=['Fecha'])  # Eliminar filas con fechas inválidas

            # Calcular rango de fechas después de modificaciones
            date_min = df['Fecha'].min()
            date_max = df['Fecha'].max()
        else:
            date_min = None
            date_max = None

        # Eliminar filas con valores NaN en otras columnas
        df = df.dropna()

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

        # Calcular estadísticas personalizadas
        if not df_stats.empty:
            custom_percentiles = [0.5, 0.75, 0.99]
            percentiles = df_stats.quantile(custom_percentiles).transpose()
            percentiles.columns = [f"Percentil {int(p * 100)}" for p in custom_percentiles]

            stats = pd.DataFrame({
                'Archivo': file,
                'Columna': percentiles.index,
                'Media': df_stats.mean(),
                'Desviación estándar': df_stats.std(),
                'Mínimo': df_stats.min(),
                'Máximo': df_stats.max()
            }).reset_index(drop=True)

            # Combinar con los percentiles personalizados
            stats = pd.concat([stats, percentiles.reset_index(drop=True)], axis=1)
            statistical_summaries.append(stats)
        else:
            print(f"Sin datos para estadísticas en el archivo: {file}")

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
if statistical_summaries:
    stats_summary_df = pd.concat(statistical_summaries, ignore_index=True)
    stats_output_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_proceso_count\statistical_summary.csv"
    stats_summary_df.to_csv(stats_output_path, index=False)
    print(f"\nEstadísticas descriptivas guardadas en: {stats_output_path}")
else:
    print("\nNo hay estadísticas descriptivas para guardar.")
