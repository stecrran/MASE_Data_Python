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
    def __init__(self, urls):
        """
        This constructor initialises the `AnalyseCSV` class with the URLs of two CSV files: 
        'go_daily_sales' and 'go_products'. It sets up the class for data analysis by performing the following steps:

        1. Unpack the provided URLs: 
           - The first URL corresponds to the daily sales data (go_daily_sales_URL).
           - The second URL corresponds to the products data (go_products_URL).
        2. Initialise empty attributes (`self.go_daily_sales`, `self.go_products`, `self.merged_df`) to store the dataframes.
        3. Call the `getCSVFiles` method to load and analyse the CSV files.
        4. Call the `MergeDataFrame` method to merge the two datasets ('go_daily_sales' and 'go_products') into a single dataframe (`self.merged_df`) for further analysis.
        
        By the end of this process, the class will have loaded, analysed, and merged the datasets, making the data ready 
        for additional operations or visualisations.
        """

    def getCSVFiles(self):
        print("\n\nUsing tables:\ngo_daily_sales\ngo_products")
        """
        This function retrieves and processes two CSV files: 'go_daily_sales' and 'go_products'.
        It performs the following steps:

        1. Print a message to indicate which tables (CSV files) are being used.
        2. Call the `preformEDA` method for 'go_daily_sales' to load and analyse the daily sales CSV file.
        3. Call the `preformEDA` method for 'go_products' to load and analyse the products CSV file.
        
        Each CSV file is analysed for its structure and content, and the results are stored 
        in the corresponding class attributes (`self.go_daily_sales` and `self.go_products`).
        The data analysis includes printing info about the dataframe, unique values, and displaying the first and last rows.

        This function ensures that both CSV files are loaded and ready for further data analysis tasks.
        """


    def preformEDA(self, tablenme, url):
        print("\n\nEDA Output")
        """
        This function performs Exploratory Data Analysis (EDA) on a CSV file loaded from the provided URL.
        It provides insights into the dataset by printing key information about its structure and content.

        Steps:
        1. Load the CSV file into a pandas dataframe using the provided URL.
        2. Print a separator and the name of the table to clearly distinguish the output in the console.
        3. Print the dataframe's structure and metadata using .info() to display column names, data types, and memory usage.
        4. Print the number of unique items in each column using .nunique() to show how many distinct values each column contains.
        5. Apply the .unique() function to print the unique values in each column, helping to identify patterns or outliers.
        6. Display the first and last few rows of the dataframe for a quick visual snapshot using tabulate for nicely formatted output.
        7. Store the dataframe in the appropriate attribute based on the table name:
           - If the table is 'go_daily_sales', store it in self.go_daily_sales.
           - Otherwise, store it in self.go_products.

        This function helps provide a quick overview of the dataset for further analysis.
        """

    def MergeDataFrame(self):
        print("\n\nMerged Dataframe")
        """
        This function merges two dataframes: one containing product information (from go_products) and 
        another containing daily sales data (from go_daily_sales). The merge is done based on the 
        'Product number' column, creating a comprehensive dataset for further analysis.

        Steps:
        1. Extract relevant columns from the products dataframe ('Product number', 'Product', 'Unit cost').
        2. Merge the products dataframe with the daily sales dataframe based on 'Product number', 
           using an inner join to include only matching rows.
        3. Calculate additional columns:
            - 'Total Sales' by multiplying 'Quantity' with 'Unit sale price'.
            - 'Total Profit' by subtracting the total cost (unit cost * quantity) from total sales.
        4. Round the sales and profit values to two decimal places for clarity.
        5. Print the first and last rows of the merged dataframe using the printDF function for inspection.

        This merged dataframe ('self.merged_df') becomes the central dataset used for further analysis,
        such as computing total sales, profit, and quantities sold by product.
        """


    def analyseTop10QuantitySales(self):
        print("Analyse Top 10 Quantity Sales")
        """
        This function analyses the top 10 products based on total sales from the dataset.
        It performs the following steps:
        
        1. Group the merged dataframe by 'Product' to aggregate values such as the total sales, 
           total quantity sold, and total profit.
        2. Sort the products to find the top 10 products based on their total sales.
        3. Display the top 10 products in a formatted table with their respective sales and profit values.
        4. Create a bar chart to visualise the total sales and total profit for these top 10 products.
        5. Display the results in a Tkinter window with two bar charts (one for sales and one for profit).
        6. Wrap long product names to ensure the x-axis labels remain readable.
        7. Use a Tkinter canvas to show the plot with a toolbar for interaction.

        The output includes both a printed table of the top 10 products and a visual plot that 
        helps compare their sales and profit.
        """

   
    def analyseProductByID(self, prod_ID):
        print("Analyse Product by ID")
        """
        This function analyses the sales data for a specific product based on the provided product ID (prod_ID).
        It filters the data for that product, calculates relevant statistics such as total sales, profit, and the 
        number of orders. Additionally, it visualises the total sales and profit, and plots the number of orders 
        per year using a bar chart.

        Steps:
        1. Filter the dataframe for the product with the given product ID.
        2. Compute statistics like total quantity sold, total sales, total profit, and number of orders.
        3. Display the statistics in a formatted table.
        4. Plot the total sales and profit in a bar chart.
        5. Plot the total orders per year on a line chart.
        6. Create a Tkinter window to show the charts.
        """

    def printDF(self, dataF):
        """
        This function prints the first and last few rows of a given dataframe in a nicely formatted way.
        It uses the `tabulate` library to format the output, making it easier to read.

        Steps:
        1. Print the first five rows of the dataframe using `dataF.head()`.
        2. Print the last five rows of the dataframe using `dataF.tail()`.
        3. The `tabulate` function is used to format the dataframe into a pretty table, including column headers and index values.
        4. Add a newline for better separation in the console output after displaying the dataframe.

        This function provides a quick overview of the content of the dataframe, ensuring that both the start and end of the data can be easily inspected.
        """
