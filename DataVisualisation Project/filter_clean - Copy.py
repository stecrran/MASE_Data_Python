import pandas as pd

def performEDA():
    # Load the CSV files
    df_business = pd.read_csv('filtered_data.csv')
    df_movieNames = pd.read_csv('movies_names.csv')
    df_moviesGenre = pd.read_csv('movies_genre.csv')

    # Extract the relevant 'GR: USD...' part in 'businesstext'
    df_business['businesstext'] = df_business['businesstext'].str.extract(r'(GR:.*?USD.*?)(?=\s*GR:|\s*$)', expand=False)

    # Drop rows with NaN in 'businesstext' column
    df_business = df_business.dropna(subset=['businesstext'])

    # Extract the numerical value from the 'businesstext' and create a new column
    df_business['usd_value'] = df_business['businesstext'].str.extract(r'USD\s*([\d,]+)')[0]

    # Remove commas from the extracted numbers and convert to float for consistency
    df_business['usd_value'] = df_business['usd_value'].str.replace(',', '').astype(float)

    # Export to a new CSV file
    df_business.to_csv('gross_USD_by_movieID.csv', index=False)

    # Merge `df_business` with `df_movieNames` based on 'movieid'
    merged_df = pd.merge(df_business, df_movieNames, on='movieid', how='inner')

    # Return the merged DataFrame and the genre DataFrame for further use
    return merged_df, df_moviesGenre

def performMerge(merged_df, df_moviesGenre):
    # Merge the `merged_df` with `df_moviesGenre` based on 'movieid'
    merged_df_genre = pd.merge(merged_df, df_moviesGenre, on='movieid', how='inner')

    # Export the final merged DataFrame to a new CSV file
    merged_df_genre.to_csv('merge_genre.csv', index=False)

# Run the functions directly
merged_df, df_moviesGenre = performEDA()  # Run performEDA and capture the DataFrames
performMerge(merged_df, df_moviesGenre)   # Run performMerge with the DataFrames
