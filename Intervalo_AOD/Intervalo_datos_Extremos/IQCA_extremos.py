import pandas as pd

# Cargar el archivo CSV
ruta_archivo = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos_Extremos\PM2.5_UTC.csv"
df = pd.read_csv(ruta_archivo, low_memory=False)

# Convertir la columna de fecha a formato datetime
df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

# Filtrar los datos a partir del año 2018
df = df[df['Fecha'].dt.year >= 2018]

# Reiniciar el índice para evitar problemas de índice desordenado
df.reset_index(drop=True, inplace=True)

# Convertir todas las columnas (excepto la de fecha) a números, ignorando errores
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Definir los rangos y sus etiquetas
niveles = {
    "Precaucion": (51, 150),
    "Alerta": (151, 250),
    "Alarma": (251, 350),
    "Emergencia": (350, float('inf'))
}

# Función para clasificar valores según el nivel
def clasificar(valor):
    for nivel, (minimo, maximo) in niveles.items():
        if minimo <= valor < maximo:
            return nivel
    return None

# Identificar filas y columnas que cumplen con los rangos
resultados = []
for col in df.columns[1:]:
    for idx, valor in df[col].dropna().items():
        nivel = clasificar(valor)
        if nivel:
            print(f"Fecha: {df.iloc[idx, 0]}, Estacion: {col}, Valor: {valor}, Nivel: {nivel}")  # Verifica los valores procesados
            resultados.append({"Fecha": df.iloc[idx, 0], "Estacion": col, "Nivel": nivel, "Valor": valor})

# Crear un DataFrame con los resultados
resultados_df = pd.DataFrame(resultados)

# Verifica si resultados_df tiene datos
if not resultados_df.empty:
    print(resultados_df)
    alarma_df = resultados_df[resultados_df["Nivel"] == "Alerta"]
    print(alarma_df)
else:
    print("No se encontraron resultados.")
# Guardar los resultados en un archivo CSV
resultados_df.to_csv(r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos_Extremos\IQCA_Extremos.csv", index=False)
