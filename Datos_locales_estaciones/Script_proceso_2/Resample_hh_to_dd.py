# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 23:44:14 2024

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
        'NO2': 'mean',
        'O3': 'mean',
        'PM25': 'mean',
        'PRE': 'mean',
        'RS': 'mean',
        'SO2': 'mean',
        'TMP': 'mean',
        'VEL': 'mean',
        'CO': 'mean',
        'DIR': 'mean',
        'HUM': 'mean',
        'LLU': 'sum'
    }

    # Eliminar columnas que no existen en el DataFrame
    operaciones = {col: op for col, op in operaciones.items() if col in df.columns}

    # Resample y procesamiento de los datos
    df_resampled = df.resample('D').agg(operaciones)

    nueva_ruta = rf"C:\Users\ADMIN\Desktop\Documentos\Datos_locales_estaciones\Datos_proceso_2\diarios_{localidad}.csv"
    df_resampled.to_csv(nueva_ruta, index=True)