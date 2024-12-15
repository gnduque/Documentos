import pandas as pd

# Cargar el archivo CSV
ruta = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_PM25\PM25_crudos.csv"
df = pd.read_csv(ruta)

# Convertir la columna 'Fecha' al formato de fecha y hora
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d %H:%M:%S')

# Asegurarse de que las columnas de PM25 son numéricas, forzando a NaN cualquier valor no numérico
df[df.columns[1:]] = df[df.columns[1:]].apply(pd.to_numeric, errors='coerce')

# Encontrar las horas con valores máximos de PM25 para cada estación (ignorando NaN)
resultados = {}
for estacion in df.columns[1:]:
    max_idx = df[estacion].idxmax(skipna=True)  # Ignora los NaN al buscar el máximo
    resultados[estacion] = df.loc[max_idx, 'Fecha']  # Recupera la fecha correspondiente

# Mostrar los resultados
for estacion, fecha in resultados.items():
    print(f"Estación {estacion}: Máximo PM25 en {fecha}")
