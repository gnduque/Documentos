import pandas as pd

# Ruta del archivo previamente generado
ruta_original = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\PM2.5_filtrado.csv"
ruta_guardar = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\PM2.5_resample_diario.csv"

try:
    # Leer el archivo filtrado
    df = pd.read_csv(ruta_original)

    # Asegurarse de que la columna de fecha esté en formato datetime
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'])
    else:
        raise ValueError("La columna 'datetime' no existe en el archivo.")

    # Establecer la columna datetime como índice
    df.set_index('datetime', inplace=True)

    # Convertir columnas a numéricas, ignorando errores para no numéricos
    df = df.apply(pd.to_numeric, errors='coerce')

    # Realizar el resample diario tomando el promedio
    df_resample_diario = df.resample('D').mean()

    # Guardar el archivo con resample diario
    df_resample_diario.to_csv(ruta_guardar)

    print(f"Archivo generado correctamente: {ruta_guardar}")

except Exception as e:
    print(f"Error: {e}")
