from CSVObj_GoSalesTest2 import AnalyseCSV
import pandas as pd
from tabulate import tabulate


# Example driver function
def main():
    # Local file paths for the datasets
    go_daily_sales_local = "C:/Users/ohsev/Documents/SoftwareDev/MSc_Ericsson/Data Analysis + Visualisation/Project/go_daily_sales.csv"
    go_products_local = "C:/Users/ohsev/Documents/SoftwareDev/MSc_Ericsson/Data Analysis + Visualisation/Project/go_products.csv"

    # Initialize the class with required file paths
    analyser = AnalyseCSV(go_daily_sales_local, go_products_local)

    # Perform analysis on CSV files and merged data
    analyser.processCSVFiles()


if __name__ == '__main__':
    main()