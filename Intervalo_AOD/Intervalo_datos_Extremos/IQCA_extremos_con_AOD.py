import pandas as pd

# Cargar los archivos CSV
df1 = pd.read_csv('C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos_Extremos\IQCA_Extremos.csv')
df2 = pd.read_csv('C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos_Extremos\AOD_mean.csv')

# Convertir la columna 'Fecha' del primer archivo a solo fecha (sin hora)
df1['Fecha'] = pd.to_datetime(df1['Fecha']).dt.date

# Convertir la columna 'Fecha' del segundo archivo a solo fecha (sin hora)
df2['Fecha'] = pd.to_datetime(df2['Fecha']).dt.date

# Agregar la columna AOD al primer archivo según las fechas y estaciones
df1['AOD'] = df1.apply(lambda row: df2.loc[df2['Fecha'] == row['Fecha'], row['Estacion']].values[0] if not df2.loc[df2['Fecha'] == row['Fecha'], row['Estacion']].empty else None, axis=1)

# Guardar el nuevo archivo con la columna AOD
df1.to_csv('C:\\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Intervalo_AOD\\Intervalo_datos_Extremos\\IQCA_Extremos_con_AOD.csv', index=False)
