import pandas as pd
from tqdm import tqdm

localidades = ["Belisario", "Carapungo", "Centro", "Cotocollao", "ElCamal", "Guamani", "LosChillos", "SanAntonio", "Tumbaco"]

for localidad in tqdm(localidades, desc="Procesando localidades"):
    try:
        archivo = rf"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_proceso_1\{localidad}.csv"
        df = pd.read_csv(archivo, header=0, skiprows=[1])
        
        # Convertir la columna Fecha a tipo datetime
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        
        # Ajustar las fechas de UTC-5 a UTC
        df['Fecha'] = df['Fecha'] + pd.Timedelta(hours=5)
        
        # Establecer minutos y segundos a 0
        df['Fecha'] = df['Fecha'].apply(lambda fecha: fecha.replace(minute=0, second=0))
        
        # Establecer la columna Fecha como índice
        df.set_index('Fecha', inplace=True)
        
        # Asegurarse de que el índice esté en orden ascendente
        df = df.sort_index()
        
        # Convertir columnas a tipo numérico
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Crear un DataFrame vacío para almacenar los resultados
        df_resampled = pd.DataFrame()
        
        # Proceso columna por columna
        for col in df.columns:
            # Eliminar los valores NaN de la columna antes de realizar cualquier operación
            df_col = df[col].dropna()
            
            # Filtrar los días con 24 horas completas (de 0 a 23 horas)
            df_col_grouped = df_col.groupby(df_col.index.date).filter(
                lambda x: x.index.hour.min() == 0 and x.index.hour.max() == 23 and len(x) == 24
            )
            
            # Si después del filtrado el DataFrame está vacío, continuar con la siguiente columna
            if df_col_grouped.empty:
                print(f"No hay datos completos para la columna {col} en la localidad {localidad}.")
                continue
            
            # Realizar el resample y calcular la agregación (promedio o suma) para la columna
            if col == 'LLU':  # Para la columna 'LLU', se hará una suma
                df_resampled_col = df_col_grouped.resample('D').sum()
            else:  # Para las demás columnas, se calculará el promedio
                df_resampled_col = df_col_grouped.resample('D').mean()
            
            # Renombrar la columna antes de hacer el join para evitar el conflicto
            df_resampled_col.name = f"{col}_resampled"
            
            # Concatenar la columna procesada al DataFrame final
            df_resampled = pd.concat([df_resampled, df_resampled_col], axis=1)
        
        # Asegurarse de que el DataFrame final esté en orden
        df_resampled = df_resampled.sort_index()
        
        # Guardar el DataFrame procesado completo
        nueva_ruta = rf"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_proceso_2\Datos\diarios_{localidad}.csv"
        df_resampled.to_csv(nueva_ruta, index=True)
    
    except FileNotFoundError:
        print(f"Archivo no encontrado para la localidad: {localidad}.")
    except Exception as e:
        print(f"Error procesando la localidad {localidad}: {e}")
