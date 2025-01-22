import pandas as pd
import os
import calendar
from datetime import datetime

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

# Rango de meses para filtrar (de octubre a mayo)
mes_inicio = 6  # Octubre
mes_fin = 9      # Mayo

# Obtener nombres de los meses
nombre_mes_inicio = calendar.month_name[mes_inicio]  # Octubre
nombre_mes_fin = calendar.month_name[mes_fin]        # Mayo

# Crear el nombre del archivo automáticamente con los nombres de los meses
archivo_combinado = f"C:\\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Intervalo_AOD\\Intervalo_datos\\Min_Max_periodos\\Min_Max_{nombre_mes_inicio}_a_{nombre_mes_fin}.csv"

for archivo in archivos:
    try:
        # Leer el archivo CSV
        df = pd.read_csv(archivo)
        print(f"Leyendo archivo: {archivo}")
        print(df.head())  # Diagnóstico inicial

        # Verificar columnas necesarias
        columnas_necesarias = ['Fecha', 'AOD_mean'] + categorias
        if not all(col in df.columns for col in columnas_necesarias):
            print(f"El archivo {archivo} no contiene las columnas necesarias.")
            continue

        # Convertir la columna 'Fecha' a formato datetime
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

        # Filtrar por los meses de octubre a mayo
        df['Mes'] = df['Fecha'].dt.month
        df['Año'] = df['Fecha'].dt.year
        df = df[((df['Mes'] >= mes_inicio) | (df['Mes'] <= mes_fin))]

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

# Guardar resultados combinados con el rango de meses en el nombre del archivo
if not todos_los_resultados:
    print("No se generaron resultados. Verifica los datos de entrada.")
else:
    tabla_resultados = pd.DataFrame(todos_los_resultados)
    tabla_resultados.to_csv(archivo_combinado, index=False)
    print(f"Procesamiento completo. Los resultados combinados se han guardado en: {archivo_combinado}")
