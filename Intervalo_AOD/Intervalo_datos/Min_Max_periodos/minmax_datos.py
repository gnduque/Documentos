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
categorias = ['IQCA']
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
        columnas_necesarias = ['AOD_mean'] + categorias
        if not all(col in df.columns for col in columnas_necesarias):
            print(f"El archivo {archivo} no contiene las columnas necesarias.")
            continue

        # Eliminar filas con valores nulos en la columna AOD_mean
        df = df.dropna(subset=['AOD_mean'])

        # Calcular el mínimo y máximo para cada categoría de IQCA
        for categoria in categorias:
            for valor_categoria in valores_categorias:
                # Filtro por categoría
                filtro = df[df[categoria] == valor_categoria]
                if not filtro.empty:
                    minimo = filtro['AOD_mean'].min()
                    maximo = filtro['AOD_mean'].max()
                    todos_los_resultados.append({
                        'Estacion': os.path.splitext(os.path.basename(archivo))[0],
                        'Categoria': categoria,
                        'Valor Categoria': valor_categoria,
                        'AOD': 'AOD_mean',
                        'Min': minimo,
                        'Max': maximo
                    })
    except Exception as e:
        print(f"Error procesando {archivo}: {e}")

# Guardar resultados combinados
if not todos_los_resultados:
    print("No se generaron resultados. Verifica los datos de entrada.")
else:
    archivo_combinado = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos\Min_Max_periodos\Resultados_datos_AOD_mean.csv"
    tabla_resultados = pd.DataFrame(todos_los_resultados)
    tabla_resultados.to_csv(archivo_combinado, index=False)
    print(f"Procesamiento completo. Los resultados combinados se han guardado en: {archivo_combinado}")
