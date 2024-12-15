import pandas as pd

# Ruta del archivo original
ruta_original = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\PM2.5.csv"
# Ruta del archivo a guardar
ruta_guardar = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\PM2.5_filtrado.csv"

# Leer el archivo CSV
df = pd.read_csv(ruta_original)

# Convertir la primera columna a formato datetime, ajustando la zona horaria
df['datetime'] = pd.to_datetime(df.iloc[:, 0], errors='coerce').dt.tz_localize('America/Bogota').dt.tz_convert('UTC')

# Filtrar los datos desde el año 2018 en adelante
df_filtrado = df[df['datetime'] >= '2018-01-01']

# Guardar el archivo filtrado
df_filtrado.to_csv(ruta_guardar, index=False)
