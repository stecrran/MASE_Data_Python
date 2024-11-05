import pandas as pd
from tabulate import tabulate
from sqlalchemy import create_engine, inspect
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import textwrap

class AnalyseCSV:
    def __init__(self, go_daily_sales_local, go_products_local):
        # Unpack the URLs
        self.go_daily_sales_local = "C:/Users/ohsev/Documents/SoftwareDev/MSc_Ericsson/Data Analysis + Visualisation/Project/go_daily_sales.csv"
        self.go_products_local = "C:/Users/ohsev/Documents/SoftwareDev/MSc_Ericsson/Data Analysis + Visualisation/Project/go_products.csv"

        # Initialize empty attributes
        self.go_daily_sales = None
        self.go_products = None
        self.merged_df = None

        # Load and analyze the CSV files
        self.getCSVFiles()

        # Merge the datasets
        self.MergeDataFrame()

    def getCSVFiles(self):
        # Read the CSV files from the URLs
        self.go_daily_sales = pd.read_csv(self.go_daily_sales_local)
        self.go_products = pd.read_csv(self.go_products_local)


    def MergeDataFrame(self):
        # Example of merging the dataframes, assuming 'product_id' is a common key
        self.merged_df = pd.merge(self.go_daily_sales, self.go_products, on='Product number')

    def printDailySales(self):
        # Print the daily sales dataframe
        if self.go_daily_sales is not None:
            print(self.go_daily_sales.head())  # Print first 5 rows
        else:
            print("Daily sales data is not loaded.")

    def printProducts(self):
        # Print the products dataframe
        if self.go_products is not None:
            print(self.go_products.head())  # Print first 5 rows
        else:
            print("Products data is not loaded.")

    def printMergedData(self):
        # Print the merged dataframe
        if self.merged_df is not None:
            print(self.merged_df.head())  # Print first 5 rows
        else:
            print("Merged data is not available.")

    def preformEDA(self, tablenme, url):
        print("\n\nEDA Output")
        # 1. Load the CSV file into a pandas dataframe
        df = pd.read_csv(url)

        # 2. Print a separator and the name of the table
        print("\n" + "=" * 50)
        print(f"Performing EDA for self.go_daily_sales_local")
        print("=" * 50 + "\n")

        # 3. Print the dataframe's structure and metadata using .info()
        print("Dataframe Info:")
        print(df.info())
        print("\n")

        # 4. Print the number of unique items in each column using .nunique()
        print("Number of unique items in each column:")
        print(df.nunique())
        print("\n")

        # 5. Apply the .unique() function to print the unique values in each column
        print("Unique values in each column:")
        for col in df.columns:
            print(f"\nUnique values in column '{col}':")
            print(df[col].unique())
        print("\n")

        # 6. Display the first and last few rows of the dataframe using tabulate for formatted output
        print("First 5 rows of the dataframe:")
        print(tabulate(df.head(), headers='keys', tablefmt='psql'))
        print("\nLast 5 rows of the dataframe:")
        print(tabulate(df.tail(), headers='keys', tablefmt='psql'))

        # 7. Store the dataframe in the appropriate attribute based on the table name
        if table_name == 'go_daily_sales':
            self.go_daily_sales = df
        else:
            self.go_products = df

        print(f"\nData stored in {'self.go_daily_sales' if table_name == 'go_daily_sales' else 'self.go_products'}\n")