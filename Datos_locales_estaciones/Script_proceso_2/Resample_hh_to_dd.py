# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 23:44:14 2024

@author: ADMIN
"""

import pandas as pd
from tqdm import tqdm

# Leer el archivo Excel, ignorando la fila 2
archivo_excel = r"C:\Users\ADMIN\Desktop\Documentos\Datos_estaciones\Datos_proceso_1\Belisario.xlsx"
datos = pd.read_excel(archivo_excel, skiprows=[2])

# Convertir la columna "Fecha" al formato datetime
datos["Fecha"] = pd.to_datetime(datos["Fecha"])

# Establecer la columna "Fecha" como índice
datos.set_index("Fecha", inplace=True)

# Calcular el número total de días para la barra de progreso
total_dias = (datos.index.max() - datos.index.min()).days

# Crear una barra de progreso
with tqdm(total=total_dias, desc="Re-muestreo") as pbar:
    # Re-muestrear los datos para obtener valores diarios
    datos_diarios = datos.resample('D').mean()  # Re-muestreo para obtener el promedio diario
    
    # Actualizar la barra de progreso
    pbar.update(1)

# Guardar los datos re-muestreados en un nuevo archivo Excel
archivo_salida = r"C:\Users\ADMIN\Desktop\Documentos\Datos_estaciones\Datos_proceso_2\diarios_Belisario.xlsx"
datos_diarios.to_excel(archivo_salida)

print("Datos re-muestreados y guardados en", archivo_salida)
