import pandas as pd
import glob

try:
    # Define the path to the CSV files
    path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\AOD_mean_con_0'

    # Use glob to get all the CSV files in the directory
    all_files = sorted(glob.glob(path + "/*.csv"))

    # Initialize an empty list to store dataframes
    dfs = []

    # Iterate over each file
    for filename in all_files:
        # Read the CSV file
        df = pd.read_csv(filename)
        
        # Rename the column 'system:time_start' to 'Fecha' if necessary
        if 'system:time_start' in df.columns:
            df.rename(columns={'system:time_start': 'Fecha'}, inplace=True)
        
        # Ensure the 'Fecha' column is in datetime format
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%b %d, %Y')
        
        # Convert the 'Fecha' column to 'yyyy-mm-dd'
        df['Fecha'] = df['Fecha'].dt.strftime('%Y-%m-%d')
        
        # Append the dataframe to the list
        dfs.append(df)

    # Concatenate all dataframes in the list
    if dfs:
        merged_df = pd.concat(dfs)
        
        # Sort the merged dataframe by 'Fecha' to ensure chronological order
        merged_df.sort_values(by='Fecha', inplace=True)
        
        # Save the sorted dataframe to a CSV file
        output_path = r'C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Intervalo_AOD\recopila_datos\AOD_mean_con_0\AOD_mean_0.csv'
        merged_df.to_csv(output_path, index=False)
        
        print(f"The files have been successfully merged, sorted, and saved as '{output_path}'.")
    else:
        print("No dataframes to concatenate.")
except Exception as e:
    print(f"An error occurred: {e}")
