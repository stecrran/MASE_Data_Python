import pandas as pd

df_genre = pd.read_csv('merge_genre_utf8.csv')
df_financials = pd.read_csv('compare_Budget_to_Gross.csv')

def performMergeBudgetAndGross(df_genre, df_financials):
    # merge the `merged_df` with `df_moviesGenre` on 'movieid'
    merged_df_genre = pd.merge(df_genre, df_financials, on='movieid', how='inner')

    # export the merged DataFrame to a separate CSV file
    merged_df_genre.to_csv('merge_financial_byGenre.csv', index=False)


performMergeBudgetAndGross(df_genre, df_financials) # Run performMerge with the DataFrames