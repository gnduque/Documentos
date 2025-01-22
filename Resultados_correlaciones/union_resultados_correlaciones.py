import pandas as pd

# Cargar los archivos
archivos = [
    "C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Resultados_correlaciones/correlaciones_Anual.csv",
    "C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Resultados_correlaciones/correlaciones_Diaria.csv",
    "C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Resultados_correlaciones/correlaciones_Estacional.csv",
    "C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Resultados_correlaciones/correlaciones_Mensual.csv",
    "C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Resultados_correlaciones/correlaciones_Semanal.csv"
]

# Leer y combinar los archivos
dfs = []
for archivo in archivos:
    df = pd.read_csv(archivo)
    df['Archivo'] = archivo.split("/")[-1]  # Añadir columna con el nombre del archivo
    dfs.append(df)

# Concatenar todos los DataFrames
resultado = pd.concat(dfs, ignore_index=True)

# Guardar el archivo combinado
resultado.to_csv("C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Resultados_correlaciones/correlaciones_combinado.csv", index=False)
