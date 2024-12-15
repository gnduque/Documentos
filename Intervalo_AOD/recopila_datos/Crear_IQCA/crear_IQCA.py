import pandas as pd
import glob

ruta = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Crear_IQCA\*.csv"
archivos = glob.glob(ruta)

def categorizar_pm25(valor):
    if 0 <= valor <= 25:
        return "Deseable"
    elif 25 < valor <= 50:
        return "Aceptable"
    elif 50 <valor <= 150:
        return "Precaucion"
    elif 150 < valor <= 250:
        return "Alerta"
    elif 250 < valor <= 350:
        return "Alarma"
    elif valor > 350:
        return "Emergencia"
    else:
        return "Incorrecto"

for archivo in archivos:
    try:
        df = pd.read_csv(archivo)
        if 'PM25' in df.columns:
            df['IQCA'] = df['PM25'].apply(categorizar_pm25)
            if 'AQI' in df.columns:
                df = df.drop(columns=['AQI'])
            df.to_csv(archivo, index=False)
        else:
            print(f"El archivo {archivo} no tiene la columna 'PM25'.")
    except Exception as e:
        print(f"Error procesando el archivo {archivo}: {e}")

print("Procesamiento completo.")



