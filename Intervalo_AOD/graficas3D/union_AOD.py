import pandas as pd

# Lista de rutas de archivos
file_paths = [
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_periodos\promedio_con0\2024.csv',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_periodos\promedio_con0\2023.csv',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_periodos\promedio_con0\2022.csv',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_periodos\promedio_con0\2021.csv',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_periodos\promedio_con0\2020.csv',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_periodos\promedio_con0\2019.csv',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_periodos\promedio_con0\2018.csv'

]

# Lista para almacenar los DataFrames
data_frames = []

# Leer y agregar cada archivo a la lista
def process_date_column(df):
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], errors='coerce')
    return df

for file_path in file_paths:
    df = pd.read_csv(file_path)
    df = process_date_column(df)
    data_frames.append(df)

# Concatenar todos los DataFrames y ordenar por fecha
merged_df = pd.concat(data_frames)
merged_df = merged_df.sort_values(by=merged_df.columns[0]).reset_index(drop=True)

# Guardar el resultado en un archivo CSV limpio
output_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_periodos\promedio_con0\merged_data.csv'
merged_df.to_csv(output_path, index=False)


print(f"Archivo combinado guardado en: {output_path}")