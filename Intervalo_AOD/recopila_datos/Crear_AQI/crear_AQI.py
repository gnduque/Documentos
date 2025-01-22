import pandas as pd

# Rutas del archivo de entrada y salida
ruta_archivo = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Crear_AQI\PM2.5_Annual_UTC.csv"
ruta_salida = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Crear_AQI\PM2.5_Annual_UTC_AQI.csv"

# Función para clasificar AQI
def classify_aqi(valor):
    if pd.isna(valor) or valor == '':  # Manejo de valores NaN o vacíos
        return "Incorrecto"
    try:
        valor = float(valor)  # Convertir a flotante si es necesario
    except ValueError:
        return "Incorrecto"
    if 0 <= valor <= 9:
        return "Bueno"
    elif 9 < valor <= 35.4:
        return "Moderado"
    elif 35.4 < valor <= 55.4:
        return "IPGS"
    elif 55.5 < valor <= 125.4:
        return "Insalubre"
    elif 125.4 < valor <= 225.4:
        return "MuyInsalubre"
    elif valor > 222.4:
        return "Peligroso"
    else:
        return "Incorrecto"

try:
    # Leer el archivo de entrada con el delimitador correcto (coma)
    df = pd.read_csv(ruta_archivo, delimiter=",")  # Usar coma como delimitador
    
    # Lista de columnas que representan estaciones
    estaciones = ['Belisario', 'Carapungo', 'Centro', 'Cotocollao', 'ElCamal', 
                  'Guamani', 'LosChillos', 'SanAntonio', 'Tumbaco']
    
    # Crear columna de categoría para cada estación, insertándola junto a la columna original
    for estacion in estaciones:
        if estacion in df.columns:  # Verificar si la estación está en el DataFrame
            categoria_col = f"AQI_{estacion}"
            df[categoria_col] = df[estacion].apply(classify_aqi)
            
            # Reordenar columnas para colocar la categoría junto a la estación
            estacion_index = df.columns.get_loc(estacion)
            cols = df.columns.tolist()
            cols.insert(estacion_index + 1, cols.pop(cols.index(categoria_col)))
            df = df[cols]
    
    # Guardar el archivo de salida
    df.to_csv(ruta_salida, index=False)
    print("Archivo actualizado guardado en:", ruta_salida)

except Exception as e:
    print(f"Error procesando el archivo {ruta_archivo}: {e}")
