import pandas as pd
from tqdm import tqdm

# Lista de estaciones
estaciones = ["Belisario", "Carapungo", "Centro", "Cotocollao", "ElCamal", "Guamani", "LosChillos", "SanAntonio", "Tumbaco"]

# Define file paths
input_file1 = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_proceso_2\AOD_mean.csv"

# Fecha mínima para filtrar
fecha_min = "2004-09-01"

for estacion in tqdm(estaciones, desc="Procesando estaciones"):
    input_file2 = rf"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_proceso_2\diarios_{estacion}.csv"
    output_file = rf"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datosproceso_3\{estacion}.csv"

    # Leer el primer archivo CSV (AOD_mean)
    df1 = pd.read_csv(input_file1)
    
    # Filtrar solo las columnas de la estación actual y la fecha
    if 'Fecha' in df1.columns and estacion in df1.columns:
        df1 = df1[['Fecha', estacion]]
    else:
        print(f"Advertencia: La columna 'Fecha' o '{estacion}' no está en el archivo {input_file1}.")
        continue

    # Renombrar las columnas para facilitar el manejo
    df1.rename(columns={estacion: 'AOD'}, inplace=True)

    # Leer el segundo archivo CSV (diarios_estacion)
    df2 = pd.read_csv(input_file2)

    # Asegurarse de que las fechas estén en el mismo formato
    df1['Fecha'] = pd.to_datetime(df1['Fecha'], errors='coerce')
    df2['Fecha'] = pd.to_datetime(df2['Fecha'], errors='coerce')

    # Filtrar por fecha mínima
    df1 = df1[df1['Fecha'] >= fecha_min]
    df2 = df2[df2['Fecha'] >= fecha_min]

    # Hacer el merge basado en la fecha
    df_resultado = pd.merge(df2, df1, on='Fecha', how='inner')

    # Guardar el resultado en un nuevo archivo CSV
    df_resultado.to_csv(output_file, index=False)