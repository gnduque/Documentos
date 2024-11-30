import pandas as pd
import os

# Ruta base
base_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Resultados_correlaciones"

# Lista de nombres de archivos
file_names = [
    "AOD_Correlations_Weekly_Mean_NoZeroAOD.csv",
    "AOD_Correlations_Periods_Mean.csv",
    "AOD_Correlations_Periods_Mean_NoZeroAOD.csv",
    "AOD_Correlations_Monthly_Mean_NoZeroAOD.csv",
    "AOD_Correlations_Mean_Weekly.csv",
    "AOD_Correlations_Mean_Monthly.csv",
    "AOD_Correlations_Mean_Annual.csv",
    "AOD_Correlations_Max_Weekly.csv",
    "AOD_Correlations_Max_Seasonal.csv",
    "AOD_Correlations_Max_Monthly.csv",
    "AOD_Correlations_Max_Annual.csv",
    "AOD_Correlations_Annual_Mean_NoZeroAOD.csv"
]

# DataFrame vacío para combinar los resultados
combined_df = pd.DataFrame()

# Iterar sobre cada archivo
for file_name in file_names:
    # Construir la ruta completa
    file_path = os.path.join(base_path, file_name)

    # Leer archivo
    df = pd.read_csv(file_path, index_col=0)

    # Extraer información del nombre del archivo
    method = "mean" if "Mean" in file_name else "max"
    frequency = (
        "weekly" if "Weekly" in file_name else
        "monthly" if "Monthly" in file_name else
        "annual" if "Annual" in file_name else
        "seasonal"
    )
    aod_filter = "NoZeroAOD" if "NoZeroAOD" in file_name else "AllAOD"

    # Añadir columnas de metadata
    df["Method"] = method
    df["Frequency"] = frequency
    df["AOD_Filter"] = aod_filter

    # Añadir al DataFrame combinado
    combined_df = pd.concat([combined_df, df])

# Guardar el archivo combinado
output_path = os.path.join(base_path, "Combined_AOD_Correlations.csv")
combined_df.to_csv(output_path)

print(f"Archivo combinado guardado en: {output_path}")
