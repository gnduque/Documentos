import pandas as pd

# Cargar el archivo CSV, ignorando los espacios en blanco iniciales y finales en los datos
file_path = 'C:\\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Intervalo_AOD\\recopila_datos\\Datos_PM25\\PM25_crudos.csv'
df = pd.read_csv(file_path, skipinitialspace=True)

# Asegurarse de que la columna 'Fecha' esté en el formato correcto
df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

# Eliminar filas con fechas no válidas
df = df.dropna(subset=['Fecha'])

# Filtrar los datos para obtener solo los registros de las 18:00 (6:00 pm) a partir del año 2018
filtered_df = df[(df['Fecha'].dt.hour == 18) & (df['Fecha'].dt.year >= 2018)]

# Guardar los datos filtrados en un nuevo archivo CSV
output_path = 'C:\\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Intervalo_AOD\\recopila_datos\\Datos_PM25\\PM25_18_utc5.csv'
filtered_df.to_csv(output_path, index=False)

print(f"Los datos filtrados se han guardado en {output_path}.")
