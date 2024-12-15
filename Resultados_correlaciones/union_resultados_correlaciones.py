import pandas as pd
import os

# Ruta base del directorio
base_dir = "C:/Users/gisse/OneDrive/Escritorio/Repositorio/Documentos/Resultados_correlaciones/"

# Lista de nombres de archivos y sus categorías
file_info = [
    ("AOD_Correlations_Max_Annual.csv", "Max", "Annual"),
    ("AOD_Correlations_Max_Monthly.csv", "Max", "Monthly"),
    ("AOD_Correlations_Max_Seasonal.csv", "Max", "Seasonal"),
    ("AOD_Correlations_Max_Weekly.csv", "Max", "Weekly"),
    ("AOD_Correlations_Mean_Annual_NoZeroAOD.csv", "Mean", "Annual_NoZeroAOD"),
    ("AOD_Correlations_Mean_Annual.csv", "Mean", "Annual"),
    ("AOD_Correlations_Mean_Monthly__NoZeroAOD.csv", "Mean", "Monthly_NoZeroAOD"),
    ("AOD_Correlations_Mean_Monthly.csv", "Mean", "Monthly"),
    ("AOD_Correlations_Mean_Seasonal_NoZeroAOD.csv", "Mean", "Seasonal_NoZeroAOD"),
    ("AOD_Correlations_Mean_Seasonal.csv", "Mean", "Seasonal"),
    ("AOD_Correlations_Mean_Weekly__NoZeroAOD.csv", "Mean", "Weekly_NoZeroAOD"),
    ("AOD_Correlations_Mean_Weekly.csv", "Mean", "Weekly")
]

# Leer y concatenar todos los archivos CSV con columnas adicionales para categoría y tipo
df_list = []
for file_name, category, period in file_info:
    file_path = os.path.join(base_dir, file_name)
    df = pd.read_csv(file_path)
    df['Category'] = category
    df['Period'] = period
    df_list.append(df)

combined_df = pd.concat(df_list)

# Guardar el dataframe combinado en un nuevo archivo CSV
output_path = os.path.join(base_dir, "Correlations_AOD.csv")
combined_df.to_csv(output_path, index=False)

print(f"Todos los archivos de correlaciones se han combinado y guardado en {output_path} con las categorías correspondientes.")
