import pandas as pd

def performEDA():
    # Load the CSV files
    df_business = pd.read_csv('filtered_data.csv')
    df_movieNames = pd.read_csv('movies_names.csv')
    df_moviesGenre = pd.read_csv('movies_genre.csv')

    # extract 'GR: USD[number]' in 'businesstext'
    df_business['businesstext'] = df_business['businesstext'].str.extract(r'(GR:.*?USD.*?)(?=\s*GR:|\s*$)', expand=False)

    # drop rows with NaN in 'businesstext'
    df_business = df_business.dropna(subset=['businesstext'])

    # extract numerical values from the 'businesstext' and create a new column
    df_business['usd_value'] = df_business['businesstext'].str.extract(r'USD\s*([\d,]+)')[0]

    # remove commas from the extracted numbers and convert to a float for consistency
    df_business['usd_value'] = df_business['usd_value'].str.replace(',', '').astype(float)

    # export to CSV file
    df_business.to_csv('gross_USD_by_movieID.csv', index=False)

    # merge `df_business` with `df_movieNames` on 'movieid'
    merged_df = pd.merge(df_business, df_movieNames, on='movieid', how='inner')

    # return the merged DataFrame and the genre DataFrame
    return merged_df, df_moviesGenre

def performMergeGenre(merged_df, df_moviesGenre):
    # merge the `merged_df` with `df_moviesGenre` on 'movieid'
    merged_df_genre = pd.merge(merged_df, df_moviesGenre, on='movieid', how='inner')

    # export the merged DataFrame to a separate CSV file
    merged_df_genre.to_csv('merge_genre.csv', index=False)


merged_df, df_moviesGenre = performEDA()  # Run performEDA and capture the DataFrames
performMergeGenre(merged_df, df_moviesGenre)  # Run performMerge with the DataFrames
