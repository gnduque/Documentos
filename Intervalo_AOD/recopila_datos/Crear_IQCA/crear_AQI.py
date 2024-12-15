import pandas as pd

def classify_aqi(pm25_value):
    if pm25_value <= 9.0:
        return "Good"
    elif pm25_value <= 35.4:
        return "Moderate"
    elif pm25_value <= 55.4:
        return "USensitiveG"
    elif pm25_value <= 125.4:
        return "Unhealthy"
    elif pm25_value <= 225.4:
        return "Very_Unhealthy"
    else:
        return "Hazardous"

# Lista de rutas de archivos
file_paths = [
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Crear_IQCA\Belisario.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Crear_IQCA\Carapungo.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Crear_IQCA\Centro.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Crear_IQCA\Cotocollao.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Crear_IQCA\ElCamal.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Crear_IQCA\Guamani.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Crear_IQCA\Tumbaco.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Crear_IQCA\LosChillos.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\Crear_IQCA\SanAntonio.csv"
]

# Iterar sobre cada archivo
for file_path in file_paths:
    df = pd.read_csv(file_path)
    df['AQI'] = df['PM25'].apply(classify_aqi)
    df.to_csv(file_path, index=False)
