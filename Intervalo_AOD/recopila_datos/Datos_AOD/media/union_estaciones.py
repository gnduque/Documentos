import pandas as pd
import os

# Lista de archivos con los datos
file_paths = [
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_AOD\media\Belisario.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_AOD\media\Carapungo.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_AOD\media\Centro.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_AOD\media\Cotocollao.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_AOD\media\ElCamal.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_AOD\media\Guamani.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_AOD\media\LosChillos.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_AOD\media\SanAntonio.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_AOD\media\Tumbaco.csv"
]

# Crear un dataframe vacío
df_final = pd.DataFrame()

# Procesar cada archivo CSV
for file in file_paths:
    # Leer cada archivo CSV
    df = pd.read_csv(file)
    
    # Convertir la columna 'Fecha' al formato deseado (yyyy-mm-dd)
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%b %d, %Y').dt.strftime('%Y-%m-%d')
    
    # Extraer el nombre de la estación del nombre del archivo
    station_name = os.path.basename(file).replace('.csv', '')
    
    # Renombrar la columna 'AOD_mean' con el nombre de la estación
    df.rename(columns={'AOD_mean': station_name}, inplace=True)
    
    # Agregar los datos al dataframe final, haciendo un 'merge' en base a la columna 'Fecha'
    if df_final.empty:
        df_final = df
    else:
        df_final = pd.merge(df_final, df, on='Fecha', how='outer')

# Guardar el dataframe final en un nuevo archivo CSV
df_final.to_csv(r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_AOD\media\AOD_mean.csv', index=False)

print("El archivo CSV unido ha sido generado correctamente.")
