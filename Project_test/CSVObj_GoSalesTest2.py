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
        # Unpack the local file paths
        self.go_daily_sales_local = go_daily_sales_local
        self.go_products_local = go_products_local

        # Initialize empty attributes
        self.go_daily_sales = None
        self.go_products = None
        self.merged_df = None

        # Load and analyze the CSV files
        self.getCSVFiles()

        # Merge the datasets
        self.MergeDataFrame()

    def getCSVFiles(self):
        # Read the CSV files from the local paths
        self.go_daily_sales = pd.read_csv(self.go_daily_sales_local)
        self.go_products = pd.read_csv(self.go_products_local)

    def MergeDataFrame(self):
        # Merge the dataframes, assuming 'Product number' is a common key
        try:
            self.merged_df = pd.merge(self.go_daily_sales, self.go_products, on='Product number')
            print("Datasets merged successfully.")
        except KeyError:
            print("Error: The key 'Product number' does not exist in both datasets. Please check the column names.")


    def performEDA(self, df, dataset_name):
        # 1. Print a separator and the name of the table
        print("\n" + "=" * 50)
        print(f"Performing EDA for {dataset_name}")
        print("=" * 50 + "\n")

        # 2. Print the dataframe's structure and metadata using .info()
        print("Dataframe Info:")
        df.info()
        print("\n")

        # 3. Print the number of unique items in each column using .nunique()
        print("Number of unique items in each column:")
        print(df.nunique())
        print("\n")

        # 4. Apply the .unique() function to print the unique values in each column
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

    def processCSVFiles(self):
        # Perform EDA on the individual datasets and the merged dataset
        print("\nAnalyzing 'go_daily_sales':")
        self.performEDA(self.go_daily_sales, 'go_daily_sales')

        print("\nAnalyzing 'go_products':")
        self.performEDA(self.go_products, 'go_products')

        if self.merged_df is not None:
            print("\nAnalyzing merged dataset:")
            self.performEDA(self.merged_df, 'merged_df')


