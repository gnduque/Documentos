import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv(r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\PM2.5.csv')

# Convertir la columna Fecha a tipo datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Ajustar la zona horaria (de UTC-5 a UTC)
df['Fecha'] = df['Fecha'] + pd.Timedelta(hours=5)

# Guardar el archivo con la nueva fecha
df.to_csv(r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\PM2.5_UTC.csv', index=False)
