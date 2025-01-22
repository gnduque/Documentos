import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv(r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos_Extremos\IQCA_Extremos_con_AOD.csv')

# Asegurarse de que la columna 'Fecha' está en formato datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Extraer el año de la columna 'Fecha'
df['Año'] = df['Fecha'].dt.year

# Filtrar los valores de AOD que sean diferentes de 0
df = df[df['AOD'] != 0]

# Agrupar por Año, Estación, y categoría de IQCA y calcular los valores máximos y mínimos de AOD
pivot_df = df.pivot_table(index=['Año', 'Estacion'], 
                          columns='IQCA', 
                          values='AOD', 
                          aggfunc=['min', 'max'])

# Limpiar los nombres de las columnas (para que sea más fácil de leer)
pivot_df.columns = [f"{col[0]}_{col[1]}" for col in pivot_df.columns]

# Resetear el índice para que sea más legible
pivot_df.reset_index(inplace=True)

# Guardar el resultado en un nuevo archivo CSV
pivot_df.to_csv(r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos_Extremos\matriz_IQCA_Extremos_sinCero.csv', index=False)

print("El archivo se ha guardado correctamente.")
