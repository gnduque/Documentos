import pandas as pd

# Ruta del archivo CSV
file_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_PM25\PM2.5_UTC.csv"

# Leer el archivo CSV con detección automática del separador
data = pd.read_csv(file_path, sep=None, engine='python')

# Asegurarse de que los nombres de las columnas están limpios
data.rename(columns=lambda x: x.strip(), inplace=True)

# Verificar si la columna 'Fecha' existe
if 'Fecha' not in data.columns:
    raise KeyError("La columna 'Fecha' no se encuentra en los datos. Verifica el archivo CSV.")

# Convertir la columna 'Fecha' a formato datetime
data['Fecha'] = pd.to_datetime(data['Fecha'], errors='coerce')

# Eliminar filas donde 'Fecha' sea inválida (NaT)
data.dropna(subset=['Fecha'], inplace=True)

# Convertir columnas no numéricas (excepto 'Fecha') a numéricas
for col in data.columns:
    if col != 'Fecha':  # Ignorar la columna de fecha
        data[col] = pd.to_numeric(data[col], errors='coerce')

# Establecer 'Fecha' como índice
data.set_index('Fecha', inplace=True)

# Realizar el resample diario (promedio)
daily_data = data.resample('D').mean()

# Guardar el resultado en un nuevo archivo CSV
output_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Datos_PM25\PM2.5_Daily_Average.csv"
daily_data.to_csv(output_path)

print(f"Resample diario completado. Archivo guardado en: {output_path}")
