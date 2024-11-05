from CSVObj_GoSales import AnalyseCSV
import pandas as pd
from tabulate import tabulate

def main():
    print("Getting CSV files from server")
    """
    This is the main entry point of the program. It performs the following steps:

    1. Define the URLs for two CSV files:
        - 'go_daily_sales_URL' points to the daily sales data.
        - 'go_products_URL' points to the product information.
    2. Pack these URLs into a tuple (`csvFiles`) to pass them as a single argument.
    3. Create an instance of the `AnalyseCSV` class, passing the `csvFiles` tuple, which loads and merges the data.
    4. Call methods from the `AnalyseCSV` instance:
        - `analyseTop10QuantitySales()` to analyse and display the top 10 products by sales.
        - `analyseProductByID(5110)` to analyse sales data for the product with ID 5110.
    5. Print a message indicating the closure of the connection, signaling that the tasks have completed.

    This function orchestrates the loading, analysing, and displaying of sales and product data.
    """
    print("Connection closed")

if __name__ == '__main__':
    main()