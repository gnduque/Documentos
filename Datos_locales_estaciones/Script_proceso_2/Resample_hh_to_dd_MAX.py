# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 21:40:58 2024

@author: ADMIN
"""

import pandas as pd
from tqdm import tqdm


localidades = ["Belisario","Carapungo", "Centro", "Cotocollao", "ElCamal", "Guamani", "LosChillos", "SanAntonio", "Tumbaco"]

for localidad in tqdm(localidades, desc="Procesando localidades"):
    archivo = rf"C:\Users\ADMIN\Desktop\Documentos\Datos_locales_estaciones\Datos_proceso_1\{localidad}.xlsx"
    df = pd.read_excel(archivo, header=0, skiprows=[1])
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Fecha'] = df['Fecha'].apply(lambda fecha: fecha.replace(minute=0, second=0))
    df.set_index('Fecha', inplace=True)

    # Diccionario de operaciones predeterminadas
    operaciones = {
        'NO2': 'max',
        'O3': 'max',
        'PM25': 'max',
        'PRE': 'max',
        'RS': 'max',
        'SO2': 'max',
        'TMP': 'max',
        'VEL': 'max',
        'CO': 'max',
        'DIR': 'mean',
        'HUM': 'max',
        'LLU': 'sum'
    }

    # Eliminar columnas que no existen en el DataFrame
    operaciones = {col: op for col, op in operaciones.items() if col in df.columns}

    # Resample y procesamiento de los datos
    df_resampled = df.resample('D').agg(operaciones)

    nueva_ruta = rf"C:\Users\ADMIN\Desktop\Documentos\Datos_locales_estaciones\Datos_proceso_2\diarios_max_{localidad}.csv"
    df_resampled.to_csv(nueva_ruta, index=True)