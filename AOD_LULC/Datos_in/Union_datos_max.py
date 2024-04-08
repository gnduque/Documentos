# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 23:19:28 2024

@author: ADMIN
"""

import pandas as pd

# Define file paths
input_file1 = "C:/Users/ADMIN/Desktop/Documentos/Descarga_AOD_GEE_MODIS/AOD_pixel_values.csv"
input_file2 = "C:/Users/ADMIN/Desktop/Documentos/Datos_locales_estaciones/Datos_proceso_2/diarios_max_ElCamal.csv"
output_file = "C:/Users/ADMIN/Desktop/Documentos/AOD_LULC/Datos_in/Max_ElCamal.csv"

# Read the first CSV file and select the 'ElCamal' column
# For tqdm, we'll add it in the final version to track progress
df1 = pd.read_csv(input_file1, usecols=['ElCamal'])

# Read the second CSV file
df2 = pd.read_csv(input_file2)

# Rename the column 'ElCamal' to 'AOD'
df1.rename(columns={'ElCamal': 'AOD'}, inplace=True)

# Append the 'AOD' column to the second dataframe
df2 = pd.concat([df2, df1], axis=1)

# Save the result to a new CSV file
# Here too, tqdm will be added in the final version
df2.to_csv(output_file, index=False)
