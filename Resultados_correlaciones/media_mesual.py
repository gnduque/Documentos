import pandas as pd

# Define el rango de fechas
inicio_fecha = '2019-01-01'
fin_fecha = '2022-01-01'

# Lista de archivos (asegúrate de definir las rutas adecuadamente)
archivos = {
    'Belisario': 'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Datos_locales_estaciones/Datosproceso_3/resample/Belisario_Resample_Mensual.csv',
    'Carapungo': 'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Datos_locales_estaciones/Datosproceso_3/resample/Carapungo_Resample_Mensual.csv',
    'Centro': 'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Datos_locales_estaciones/Datosproceso_3/resample/Centro_Resample_Mensual.csv',
    'Cotocollao': 'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Datos_locales_estaciones/Datosproceso_3/resample/Cotocollao_Resample_Mensual.csv',
    'ElCamal': 'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Datos_locales_estaciones/Datosproceso_3/resample/ElCamal_Resample_Mensual.csv',
    'Guamani': 'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Datos_locales_estaciones/Datosproceso_3/resample/Guamani_Resample_Mensual.csv',
    'LosChillos': 'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Datos_locales_estaciones/Datosproceso_3/resample/LosChillos_Resample_Mensual.csv',
    'SanAntonio': 'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Datos_locales_estaciones/Datosproceso_3/resample/SanAntonio_Resample_Mensual.csv',
    'Tumbaco': 'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Datos_locales_estaciones/Datosproceso_3/resample/Tumbaco_Resample_Mensual.csv'
}

# Filtrar los datos de las estaciones por el rango de fechas
def filtrar_por_fecha(df):
    # Convertir la columna 'Fecha' a tipo datetime si no lo está
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    
    # Filtrar por el rango de fechas
    df_filtrado = df[(df['Fecha'] >= inicio_fecha) & (df['Fecha'] <= fin_fecha)]
    
    # Convertir todas las columnas numéricas a tipo numérico, forzando errores a NaN
    df_filtrado = df_filtrado.apply(pd.to_numeric, errors='coerce')
    
    return df_filtrado

# Cargar y filtrar los datos de todas las estaciones
archivos_filtrados = {estacion: filtrar_por_fecha(pd.read_csv(path)) for estacion, path in archivos.items()}

# Función para calcular las correlaciones entre columnas
def calcular_correlaciones(archivos_filtrados):
    resultados_correlaciones = {}
    
    columnas_correlacion = ['NO2', 'O3', 'PM25', 'PRE', 'RS', 'SO2', 'TMP', 'VEL', 'CO', 'DIR', 'HUM', 'LLU', 'AOD']
    
    for estacion, df in archivos_filtrados.items():
        # Verificar qué columnas están disponibles en cada estación
        columnas_disponibles = [col for col in columnas_correlacion if col in df.columns]
        
        # Filtrar el DataFrame solo con las columnas disponibles
        df_filtrado = df[columnas_disponibles]
        
        # Calcular la correlación con la columna 'AOD'
        correlaciones = df_filtrado.corr()['AOD'].drop('AOD', errors='ignore')  # Excluye 'AOD' de su propia correlación
        
        # Almacenar las correlaciones en el diccionario de resultados
        resultados_correlaciones[estacion] = correlaciones
    
    # Convertir el diccionario en un DataFrame para mejor presentación
    df_resultados = pd.DataFrame(resultados_correlaciones)
    
    return df_resultados

# Calcular las correlaciones
resultados_correlaciones = calcular_correlaciones(archivos_filtrados)

# Mostrar resultados
print(resultados_correlaciones)
# Guardar los resultados en un archivo CSV
ruta_guardado = 'C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Resultados_correlaciones/correlaciones_Mensual.csv'
resultados_correlaciones.to_csv(ruta_guardado)

# Confirmar que los resultados se han guardado
print(f"Los resultados se han guardado en: {ruta_guardado}")