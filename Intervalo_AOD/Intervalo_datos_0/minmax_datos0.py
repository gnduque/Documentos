import pandas as pd
import os

# Lista de archivos CSV específicos
archivos = [
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos_0\Carapungo.csv",   
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos_0\SanAntonio.csv",  
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos_0\Tumbaco.csv", 
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos_0\Guamani.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos_0\Cotocollao.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos_0\Belisario.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos_0\Centro.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos_0\LosChillos.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos_0\ElCamal.csv"
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
        print(df.head())  # Diagnóstico inicial

        # Verificar columnas necesarias
        columnas_necesarias = ['AOD_media'] + categorias
        if not all(col in df.columns for col in columnas_necesarias):
            print(f"El archivo {archivo} no contiene las columnas necesarias.")
            continue

        # Convertir AOD_media, AOD_mediana y AOD_moda a numérico; valores no válidos serán NaN
        df['AOD_media'] = pd.to_numeric(df['AOD_media'], errors='coerce')

        # Reemplazar NaN por 0
        df['AOD_media'] = df['AOD_media'].fillna(0)


        print(f"Datos después de conversión y reemplazo de NaN:\n{df[['AOD_media']].head()}")

        # Eliminar filas con valores de 0 en todas las columnas de AOD
        df = df[(df['AOD_media'] != 0) ]
        print(f"Filas después de filtrar AOD_media != 0: {len(df)}")

        # Calcular el mínimo y máximo para cada categoría de IQCA
        for categoria in categorias:
            for valor_categoria in valores_categorias:
                for aod_col in ['AOD_media']:
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
    archivo_combinado = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos_0\Resultados_datos0_minmax.csv"
    tabla_resultados = pd.DataFrame(todos_los_resultados)
    tabla_resultados.to_csv(archivo_combinado, index=False)
    print(f"Procesamiento completo. Los resultados combinados se han guardado en: {archivo_combinado}")