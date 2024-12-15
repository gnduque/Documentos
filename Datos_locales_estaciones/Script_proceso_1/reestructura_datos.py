import pandas as pd

# Rutas a los archivos de Excel
archivos_excel = [
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\NO2.xlsx",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\O3.xlsx",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\PM2.5.xlsx",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\PRE.xlsx",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\RS.xlsx",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\SO2.xlsx",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\TMP.xlsx",
    r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_iniciales\\VEL.xlsx",
    r"C:\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Datos_locales_estaciones\\Datos_iniciales\\CO.xlsx",
    r"C:\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Datos_locales_estaciones\\Datos_iniciales\\DIR.xlsx",
    r"C:\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Datos_locales_estaciones\\Datos_iniciales\\HUM.xlsx",
    r"C:\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Datos_locales_estaciones\\Datos_iniciales\\LLU.xlsx"
]

# Nombres de las estaciones
estaciones = ["Belisario", "Carapungo", "Centro", "Cotocollao", "ElCamal", "Guamani", "LosChillos", "SanAntonio", "Tumbaco"]

# Ruta para guardar los archivos generados
ruta_guardado = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_proceso_1\datos"

# Leer el archivo "fecha.xlsx"
fecha_df = pd.read_excel(r"C:\Users\\gisse\\OneDrive\\Escritorio\\Repositorio\\Documentos\\Datos_locales_estaciones\\Datos_iniciales\\fecha.xlsx")

# Procesar cada estación
for estacion in estaciones:
    # Crear un DataFrame vacío para almacenar las columnas
    columnas_sitio = pd.DataFrame()

    # Leer cada archivo y seleccionar las columnas con el nombre de la estación de interés
    for archivo in archivos_excel:
        df = pd.read_excel(archivo)
        nombre_variable = archivo.split("\\")[-1].split(".")[0]  # Obtener el nombre de la variable del nombre del archivo
        if estacion in df.columns:  # Verificar si la columna existe en el archivo
            columnas_sitio = pd.concat([columnas_sitio, df[estacion].rename(f"{estacion}_{nombre_variable}")], axis=1)

    # Concatenar la columna "Fecha" al principio del DataFrame columnas_sitio
    columnas_sitio = pd.concat([fecha_df["Fecha"], columnas_sitio], axis=1)

    # Crear un nuevo archivo de Excel con las columnas seleccionadas si hay datos
    if not columnas_sitio.empty:
        columnas_sitio.to_excel(f"{ruta_guardado}\\{estacion}.xlsx", index=False)
    else:
        print(f"No se encontraron datos para la estación '{estacion}' en los archivos Excel.")
