import pandas as pd
import os

# Lista de archivos CSV específicos
archivos = [
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos\Carapungo.csv",   
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos\SanAntonio.csv",  
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos\Tumbaco.csv", 
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos\Guamani.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos\Cotocollao.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos\Belisario.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos\Centro.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos\LosChillos.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos\ElCamal.csv"
]

# Categorías de IQCA
categorias = ['IQCA', 'IQCA_1', 'IQCA_7', 'IQCA_14', 'IQCA_18']
valores_categorias = ['Deseable', 'Aceptable', 'Precaucion', 'Alerta', 'Alarma', 'Emergencia', 'Incorrecto']

# Lista para combinar todos los resultados
todos_los_resultados = []

for archivo in archivos:
    try:
        # Leer el archivo CSV
        df = pd.read_csv(archivo)
        print(f"Leyendo archivo: {archivo}")
        
        # Verificar columnas necesarias
        columnas_necesarias = ['Fecha', 'AOD_media', 'AOD_mediana', 'AOD_moda'] + categorias
        if not all(col in df.columns for col in columnas_necesarias):
            print(f"El archivo {archivo} no contiene las columnas necesarias.")
            continue

        # Convertir la columna Fecha a tipo datetime
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

        # Filtrar por el rango de fechas del 1 de marzo al final de junio del año 2024
       # df = df[((df['Fecha'].dt.year == 2020) & (df['Fecha'].dt.month == 12)) | 
         #        ((df['Fecha'].dt.year == 2021) & (df['Fecha'].dt.month <= 2))]       
        df = df[(df['Fecha'].dt.year == 2021) & (df['Fecha'].dt.month >= 6) & (df['Fecha'].dt.month <= 8)]
        if df.empty:
            print(f"No hay datos en el rango de fechas para el archivo {archivo}.")
            continue

        # Convertir AOD_media, AOD_mediana y AOD_moda a numérico; valores no válidos serán NaN
        for col in ['AOD_media', 'AOD_mediana', 'AOD_moda']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Eliminar filas con valores de 0 en todas las columnas de AOD
        df = df[(df['AOD_media'] != 0) & (df['AOD_mediana'] != 0) & (df['AOD_moda'] != 0)]
        if df.empty:
            print(f"No quedan datos válidos después de filtrar AOD en el archivo {archivo}.")
            continue

        # Calcular el mínimo y máximo para cada categoría de IQCA
        for categoria in categorias:
            for valor_categoria in valores_categorias:
                for aod_col in ['AOD_media', 'AOD_mediana', 'AOD_moda']:
                    filtro = df[df[categoria] == valor_categoria]
                    if not filtro.empty:
                        minimo = filtro[aod_col].min()
                        maximo = filtro[aod_col].max()
                        todos_los_resultados.append({
                            'Estacion': os.path.splitext(os.path.basename(archivo))[0],
                            'Categoria': categoria,
                            'Valor Categoria': valor_categoria,
                            'AOD': aod_col,
                            'Min': minimo,
                            'Max': maximo
                        })
    except Exception as e:
        print(f"Error procesando {archivo}: {e}")

# Guardar resultados combinados
if not todos_los_resultados:
    print("No se generaron resultados. Verifica los datos de entrada.")
else:
    archivo_combinado = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos\Min_Max_periodos\Resultados_minmax_periodos.csv"
    tabla_resultados = pd.DataFrame(todos_los_resultados)
    tabla_resultados.to_csv(archivo_combinado, index=False)
    print(f"Procesamiento completo. Los resultados combinados se han guardado en: {archivo_combinado}")
