import pandas as pd

def main():

    df1 = pd.read_csv('file1.csv')
    df2 = pd.read_csv('file2.csv')
    df3 = pd.read_csv('file3.csv')
    df4 = pd.read_csv('file4.csv')

    # stack them on top of each other (vertically)
    merged_dfs = pd.concat([df1, df2, df3, df4], ignore_index=True)

    # merge on common field - for example 'ID'
    merged_df = pd.merge(df1, df2, on='ID')
    merged_df = pd.merge(merged_df, df3, on='ID')

    # if there are specific columns you want to use
    merged_df = pd.merge(merged_df, df4[['Product number', 'Date', 'Quantity', 'Unit price', 'Unit sale price']], on='Product number')



if __name__=='__main__':
    main()