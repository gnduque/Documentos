import pandas as pd

# Cargar los datos de AOD media
mean_aod_path = 'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Intervalo_AOD/Intervalo_datos/mean/AOD_mean.csv'
mean_aod_df = pd.read_csv(mean_aod_path)

# Lista de archivos de estaciones
station_files = [
    'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Intervalo_AOD/Intervalo_datos/Carapungo.csv',
    'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Intervalo_AOD/Intervalo_datos/SanAntonio.csv',
    'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Intervalo_AOD/Intervalo_datos/Tumbaco.csv',
    'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Intervalo_AOD/Intervalo_datos/Guamani.csv',
    'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Intervalo_AOD/Intervalo_datos/Cotocollao.csv',
    'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Intervalo_AOD/Intervalo_datos/Belisario.csv',
    'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Intervalo_AOD/Intervalo_datos/Centro.csv',
    'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Intervalo_AOD/Intervalo_datos/LosChillos.csv',
    'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Intervalo_AOD/Intervalo_datos/ElCamal.csv'
]

# Función para actualizar la columna AOD_media
def update_aod_media(station_file, mean_aod_df):
    station_df = pd.read_csv(station_file)
    station_name = station_file.split('/')[-1].split('.')[0]
    
    # Asegurarse de que la columna de fecha esté en formato datetime para ambos dataframes
    station_df['date'] = pd.to_datetime(station_df['date'])
    mean_aod_df['date'] = pd.to_datetime(mean_aod_df['date'])
    
    # Unir los dataframes por la fecha
    merged_df = pd.merge(station_df, mean_aod_df[['date', station_name]], on='date', how='left')
    
    # Actualizar la columna AOD_media con los valores correspondientes de la estación
    merged_df['AOD_media'] = merged_df[station_name]
    
    # Eliminar la columna extra de la estación
    merged_df.drop(columns=[station_name], inplace=True)
    
    # Guardar el dataframe actualizado de nuevo en el archivo CSV
    merged_df.to_csv(station_file, index=False)

# Actualizar cada archivo de estación
for station_file in station_files:
    update_aod_media(station_file, mean_aod_df)

print("Las columnas AOD_media se han actualizado correctamente.")