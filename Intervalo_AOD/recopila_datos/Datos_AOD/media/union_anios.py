import pandas as pd
import glob

try:
    # Define the path to the CSV files
    path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos_0'

    # Use glob to get all the CSV files in the directory
    all_files = glob.glob(path + "/*.csv")

    # Initialize an empty list to store dataframes
    dfs = []

    # Iterate over each file
    for filename in all_files:
        # Read the CSV file
        df = pd.read_csv(filename)
        
        # Rename the column 'system:time_start' to 'Fecha'
        df.rename(columns={'system:time_start': 'Fecha'}, inplace=True)
        
        # Convert the 'Fecha' column to datetime format and change the format to 'yyyy/mm/dd'
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%b %d, %Y').dt.strftime('%Y/%m/%d')
        
        # Append the dataframe to the list
        dfs.append(df)

    # Concatenate all dataframes in the list
    if dfs:
        merged_df = pd.concat(dfs)
        merged_df.to_csv(r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\Intervalo_datos_0\merged_data.csv', index=False)
        print("The files have been successfully merged and saved as 'merged_data.csv' in the specified location.")
    else:
        print("No dataframes to concatenate.")
except Exception as e:
    print(f"An error occurred: {e}")
