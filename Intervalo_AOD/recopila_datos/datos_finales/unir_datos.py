import pandas as pd
import os

# Paths
output_dir = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\datos_finales"
os.makedirs(output_dir, exist_ok=True)

# Input files
files = {
    "TMP": r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_TMP\TMP_daily_all_stations.csv",
    "PM25": r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_PM25\PM2.5_Daily_Average.csv",
    "AOD_mean": r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_AOD\media\AOD_mean.csv"
 #   "AOD_median": r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_AOD\mediana\AOD_median.csv",
 #  "AOD_moda": r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_AOD\moda\AOD_moda.csv"
}

# Load dataframes
data = {key: pd.read_csv(path) for key, path in files.items()}

# Filter by year >= 2018
for key in data:
    data[key]['Fecha'] = pd.to_datetime(data[key]['Fecha'], errors='coerce')
    data[key] = data[key][data[key]['Fecha'].dt.year >= 2018]

# List of stations
stations = ['Carapungo', 'SanAntonio', 'Tumbaco', 'Guamani', 'Cotocollao', 
            'Belisario', 'Centro', 'LosChillos', 'ElCamal']

# Merge and save per station
for station in stations:
    merged_df = pd.DataFrame({'Fecha': data['TMP']['Fecha']})  # or 'AOD_mean' or any file, as they all have 'Fecha'
    for key in data:
        station_data = data[key][['Fecha', station]].rename(columns={station: key})
        merged_df = pd.merge(merged_df, station_data, on='Fecha', how='left')
    
    output_path = os.path.join(output_dir, f"{station}.csv")
    merged_df.to_csv(output_path, index=False)
