import pandas as pd

# Cargar el archivo principal con las fechas y estaciones
df_aod = pd.read_csv(r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\aod_2018_2024.csv')

# Rellenar las celdas vacías con 0
df_aod.fillna(0, inplace=True)

# Filtrar para mantener solo los datos a partir de 2018
df_aod['Fecha'] = pd.to_datetime(df_aod['Fecha'])
df_aod = df_aod[df_aod['Fecha'].dt.year >= 2018]

# Lista de archivos de estaciones
estaciones_files = [
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\Belisario_daily_processed.xlsx',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\Carapungo_daily_processed.xlsx',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\Centro_daily_processed.xlsx',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\Cotocollao_daily_processed.xlsx',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\ElCamal_daily_processed.xlsx',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\Guamani_daily_processed.xlsx',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\LosChillos_daily_processed.xlsx',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\SanAntonio_daily_processed.xlsx',
    r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\Tumbaco_daily_processed.xlsx'
]

# Unir las estaciones a partir del archivo de AOD
for archivo in estaciones_files:
    df_station = pd.read_excel(archivo)
    station_name = archivo.split("\\")[-1].split("_")[0]
    
    # Asegurarse que la columna de fecha esté en ambos DataFrames
    df_station['Fecha'] = pd.to_datetime(df_station['Fecha'])
    
    # Filtrar los datos de la estación a partir de 2018
    df_station = df_station[df_station['Fecha'].dt.year >= 2018]
    
    # Unir por la fecha
    df_merged = pd.merge(df_aod[['Fecha', station_name]], df_station, on='Fecha', how='left')
    
    # Guardar el archivo con los datos fusionados
    df_merged.to_csv(f'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Basurero/{station_name}_merged.csv', index=False)