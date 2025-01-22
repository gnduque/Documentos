import pandas as pd

# Rutas a los archivos de CSV
archivos_csv = [
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\NO2.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\O3.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\PM2.5.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\PRE.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\RS.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\SO2.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\TMP.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\VEL.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\CO.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\DIR.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\HUM.csv",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\LLU.csv"
]

# Nombres de las estaciones
estaciones = ["Belisario", "Carapungo", "Centro", "Cotocollao", "ElCamal", "Guamani", "LosChillos", "SanAntonio", "Tumbaco"]

# Ruta para guardar los archivos generados
ruta_guardado = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_proceso_1\Datos"

# Procesar cada estación
for estacion in estaciones:
    # Crear un DataFrame vacío para almacenar las columnas
    columnas_sitio = None

    # Leer cada archivo y seleccionar las columnas con el nombre de la estación y "Fecha"
    for archivo in archivos_csv:
        df = pd.read_csv(archivo)
        nombre_variable = archivo.split("\\")[-1].split(".")[0]  # Obtener el nombre de la variable del nombre del archivo
        
        # Verificar si la columna de la estación existe
        if "Fecha" in df.columns and estacion in df.columns:
            # Renombrar la columna de la estación con su respectiva variable
            columna_variable = df[["Fecha", estacion]].rename(columns={estacion: f"{estacion}_{nombre_variable}"})
            
            # Unir todas las fechas posibles usando un merge
            if columnas_sitio is None:
                columnas_sitio = columna_variable
            else:
                columnas_sitio = pd.merge(columnas_sitio, columna_variable, on="Fecha", how="outer")

    # Si hay datos, ordenar por fecha y guardar
    if columnas_sitio is not None and not columnas_sitio.empty:
        columnas_sitio = columnas_sitio.sort_values(by="Fecha")  # Ordenar por fecha
        columnas_sitio.to_csv(f"{ruta_guardado}\\{estacion}.csv", index=False, encoding="utf-8-sig")
    else:
        print(f"No se encontraron datos para la estación '{estacion}' en los archivos CSV.")
