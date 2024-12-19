import pandas as pd

# Cargar los archivos CSV
matriz_df = pd.read_csv(r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Matriz_cambios\Cambios_LULC\matriz.csv')
transicion_df = pd.read_csv(r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Matriz_cambios\Cambios_LULC\Matriz_de_Transicion.csv')

# Crear un diccionario con las combinaciones y el valor de Area_km2
transicion_dict = dict(zip(transicion_df['Combinacion'], transicion_df['Area_km2']))

# Iterar sobre las columnas 1 a 10 en matriz_df
for col in range(1, 11):
    col_name = str(col)
    matriz_df[col_name] = matriz_df[col_name].apply(lambda x: transicion_dict.get(x, 0))

# Guardar el archivo resultante
output_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Matriz_cambios\Cambios_LULC\matriz_areas_km2.csv'
matriz_df.to_csv(output_path, index=False)
