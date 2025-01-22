import pandas as pd

# Rutas del archivo de entrada y salida
ruta_archivo = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Crear_IQCA\PM2.5_Daily_UTC.csv"
ruta_salida = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Crear_IQCA\PM2.5_Daily_UTC_IQCA.csv"

# Función para categorizar PM2.5
def categorizar_pm25(valor):
    if pd.isna(valor) or valor == '':  # Manejo de valores NaN o vacíos
        return "Incorrecto"
    try:
        valor = float(valor)  # Convertir a flotante si es necesario
    except ValueError:
        return "Incorrecto"
    if 0 <= valor <= 25:
        return "Deseable"
    elif 25 < valor <= 50:
        return "Aceptable"
    elif 50 < valor <= 150:
        return "Precaucion"
    elif 150 < valor <= 250:
        return "Alerta"
    elif 250 < valor <= 350:
        return "Alarma"
    elif valor > 350:
        return "Emergencia"
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
            categoria_col = f"IQCA_{estacion}"
            df[categoria_col] = df[estacion].apply(categorizar_pm25)
            
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