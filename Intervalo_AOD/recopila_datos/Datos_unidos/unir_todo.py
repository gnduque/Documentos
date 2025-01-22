import pandas as pd

# Rutas de los archivos
pm25_file = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Crear_IQCA\PM2.5_Daily_UTC_IQCA.csv"
aod_file = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_unidos\AOD_mean.csv"

# Cargar los archivos CSV
pm25_data = pd.read_csv(pm25_file)
aod_data = pd.read_csv(aod_file)

# Convertir la columna Fecha a formato de fecha para hacer la combinación
pm25_data['Fecha'] = pd.to_datetime(pm25_data['Fecha'])
aod_data['Fecha'] = pd.to_datetime(aod_data['Fecha'])

# Filtrar los datos a partir del 2004-09-01
pm25_data_filtered = pm25_data[pm25_data['Fecha'] >= '2004-09-01']
aod_data_filtered = aod_data[aod_data['Fecha'] >= '2004-09-01']

# Combinar los archivos por la columna Fecha
merged_data = pd.merge(pm25_data_filtered, aod_data_filtered, on='Fecha', how='inner')

# Reordenar las columnas según lo solicitado
ordered_columns = [
    'Fecha', 
    'Belisario', 'IQCA_Belisario', 'Belisario_AOD', 
    'Carapungo_AOD', 'Carapungo', 'IQCA_Carapungo', 
    'Centro_AOD', 'Centro', 'IQCA_Centro', 
    'Cotocollao_AOD', 'Cotocollao', 'IQCA_Cotocollao', 
    'ElCamal_AOD', 'ElCamal', 'IQCA_ElCamal', 
    'Guamani_AOD', 'Guamani', 'IQCA_Guamani', 
    'LosChillos_AOD', 'LosChillos', 'IQCA_LosChillos', 
    'SanAntonio_AOD', 'SanAntonio', 'IQCA_SanAntonio', 
    'Tumbaco_AOD', 'Tumbaco', 'IQCA_Tumbaco'
]

# Crear el archivo CSV con los datos unidos
output_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_unidos\Datos_unidos.csv"
merged_data = merged_data[ordered_columns]
merged_data.to_csv(output_path, index=False)

print(f"Archivo generado en: {output_path}")
