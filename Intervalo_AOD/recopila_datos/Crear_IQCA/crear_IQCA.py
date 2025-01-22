import pandas as pd
import os

archivos = [
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\datos_finales\Belisario.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\datos_finales\Carapungo.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\datos_finales\Centro.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\datos_finales\Cotocollao.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\datos_finales\ElCamal.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\datos_finales\Guamani.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\datos_finales\LosChillos.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\datos_finales\SanAntonio.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\datos_finales\Tumbaco.csv"
]
ruta_salida_base = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Crear_IQCA"

def categorizar_pm25(valor):
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

for archivo in archivos:
    try:
        df = pd.read_csv(archivo)
        if 'PM25' in df.columns:
            if 'AOD_mean' in df.columns:
                df = df[df['AOD_mean'] != 0]
            if 'AOD_median' in df.columns:
                df = df[df['AOD_median'] != 0]
            if 'AOD_moda' in df.columns:
                df = df[df['AOD_moda'] != 0]
            
            df['IQCA'] = df['PM25'].apply(categorizar_pm25)
            
            nombre_archivo = os.path.basename(archivo)
            ruta_salida = os.path.join(ruta_salida_base, nombre_archivo)
            df.to_csv(ruta_salida, index=False)
            print(f"Archivo actualizado guardado en: {ruta_salida}")
        else:
            print(f"El archivo {archivo} no tiene la columna 'PM25'.")
    except Exception as e:
        print(f"Error procesando el archivo {archivo}: {e}")
