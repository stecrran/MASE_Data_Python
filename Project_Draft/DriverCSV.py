from CSVObj_GoSalesTest import AnalyseCSV  # Import your class
import pandas as pd
from tabulate import tabulate  # Optional, for pretty-printing data in tabular format


def main():
    print("Getting local CSV files...")
"""
    # Initialize the AnalyseCSV object
    analyser = AnalyseCSV(go_daily_sales_local="C:/Users/ohsev/Documents/SoftwareDev/MSc_Ericsson/Data Analysis + Visualisation/Project/go_daily_sales.csv",
                          go_products_local="C:/Users/ohsev/Documents/SoftwareDev/MSc_Ericsson/Data Analysis + Visualisation/Project/go_products.csv")

    # Print the data (you can use tabulate to format it nicely if you wish)
    print("\nDaily Sales Data:")
    print(tabulate(analyser.go_daily_sales.head(), headers='keys', tablefmt='psql'))

    print("\nProduct Data:")
    print(tabulate(analyser.go_products.head(), headers='keys', tablefmt='psql'))

    print("\nMerged Data:")
    print(tabulate(analyser.merged_df.head(), headers='keys', tablefmt='psql'))
"""



if __name__ == '__main__':
    main()
