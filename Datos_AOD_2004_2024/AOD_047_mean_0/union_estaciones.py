import pandas as pd
import os

# Lista de archivos con los datos
file_paths = [
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_AOD_2004_2024\AOD_047_mean_0\Belisario_AOD_mean_0.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_AOD_2004_2024\AOD_047_mean_0\Carapungo_AOD_mean_0.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_AOD_2004_2024\AOD_047_mean_0\Centro_AOD_mean_0.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_AOD_2004_2024\AOD_047_mean_0\Cotocollao_AOD_mean_0.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_AOD_2004_2024\AOD_047_mean_0\ElCamal_AOD_mean_0.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_AOD_2004_2024\AOD_047_mean_0\Guamani_AOD_mean_0.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_AOD_2004_2024\AOD_047_mean_0\LosChillos_AOD_mean_0.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_AOD_2004_2024\AOD_047_mean_0\SanAntonio_AOD_mean_0.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_AOD_2004_2024\AOD_047_mean_0\Tumbaco_AOD_mean_0.csv"
]

# Crear un rango de fechas desde 2004-09-01 hasta hoy
date_range = pd.date_range(start="2004-09-01", end=pd.Timestamp.now().strftime('%Y-%m-%d'))

# Crear un DataFrame base con las fechas
df_final = pd.DataFrame({'Fecha': date_range.strftime('%Y-%m-%d')})

# Procesar cada archivo CSV
for file in file_paths:
    # Leer cada archivo CSV
    df = pd.read_csv(file)
    
    # Verificar que la columna 'Fecha' está correctamente en formato yyyy-mm-dd
    if 'Fecha' not in df.columns:
        raise ValueError(f"El archivo {file} no contiene una columna 'Fecha'.")
    
    # Extraer el nombre de la estación del nombre del archivo
    station_name = os.path.basename(file).replace('_AOD_mean_0.csv', '')
    
    # Renombrar la columna 'AOD_mean_0' con el nombre de la estación
    df.rename(columns={'AOD_mean_0': station_name}, inplace=True)
    
    # Hacer el merge con el DataFrame final usando 'Fecha'
    df_final = pd.merge(df_final, df[['Fecha', station_name]], on='Fecha', how='left')

# Guardar el DataFrame final en un nuevo archivo CSV
output_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_AOD_2004_2024\AOD_047_mean_0\AOD_mean_0.csv'
df_final.to_csv(output_path, index=False)

print(f"El archivo CSV unido ha sido generado correctamente: {output_path}")
