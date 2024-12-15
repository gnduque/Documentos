# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 23:19:28 2024

@author: ADMIN
"""

import pandas as pd
from tqdm import tqdm

# Lista de estaciones
estaciones = ["Belisario", "Carapungo", "Centro", "Cotocollao", "ElCamal", "Guamani", "LosChillos", "SanAntonio", "Tumbaco"]

# Define file paths
input_file1 = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Descarga_AOD_GEE_MODIS\AOD_values.csv"

for estacion in tqdm(estaciones, desc="Procesando estaciones"):
    input_file2 = rf"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datos_proceso_2\diarios_max_{estacion}.csv"
    output_file = rf"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Datos_locales_estaciones\Datosproceso_3\Max_{estacion}.csv"

    # Read the first CSV file and select the column for the current station
    df1 = pd.read_csv(input_file1, usecols=[estacion])

    # Read the second CSV file
    df2 = pd.read_csv(input_file2)

    # Rename the column to 'AOD'
    df1.rename(columns={estacion: 'AOD'}, inplace=True)

    # Append the 'AOD' column to the second dataframe
    df2 = pd.concat([df2, df1], axis=1)

    # Save the result to a new CSV file
    df2.to_csv(output_file, index=False)