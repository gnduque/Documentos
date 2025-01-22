import pandas as pd

file_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\PM2.5.csv"
output_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Basurero\PM2.5_Anual_Resample.csv"

try:
    # Leer la base de datos original
    df = pd.read_csv(file_path, dtype=str, low_memory=False)

    # Convertir la columna Fecha a datetime
    if 'Fecha' not in df.columns:
        raise ValueError("La columna 'Fecha' no está presente en los datos.")
    
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y %H:%M', errors='coerce', dayfirst=True)
    
    # Eliminar filas con fechas inválidas
    df = df.dropna(subset=['Fecha']).set_index('Fecha')

    # DataFrame para almacenar los resultados combinados
    combined_resample = pd.DataFrame()

    # Procesar cada columna por separado
    for column in df.columns:
        # Crear una copia para trabajar únicamente en la columna actual
        column_data = df[[column]].copy()

        # Convertir a numérico (ignorando errores para celdas no numéricas)
        column_data[column] = pd.to_numeric(column_data[column], errors='coerce')

        # Eliminar filas donde la columna tenga valores vacíos
        column_data = column_data.dropna()

        # Realizar resample anual
        resampled_column = column_data.resample('Y').mean()
        
        # Añadir al DataFrame combinado
        combined_resample[column] = resampled_column[column]

    # Guardar los resultados combinados en un solo archivo
    combined_resample.to_csv(output_path)
    print(f"Datos resampleados anualmente guardados en {output_path}")

except Exception as e:
    print(f"Error: {e}")
