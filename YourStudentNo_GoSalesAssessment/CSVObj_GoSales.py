import numpy as np
import pandas as pd
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from networkx.classes import non_edges
from tabulate import tabulate
from sqlalchemy import create_engine, inspect
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import textwrap

class DBConnection_Alchemy:
    def __init__(self, connect_info):
        # Unpack connection details and set up database configuration
        self.host, self.user, self.password, self.port, self.database = connect_info
        self.table = ""
        self.mydb = None
        self.connectNow()  # Initialize database connection

    def connectNow(self):
        # Printing connection details for debugging
        print(f"Attempting to connect using:\nHost: {self.host}\nUser: {self.user}\nPort: {self.port}\nDatabase: {self.database}")

        try:
            # Create SQLAlchemy engine
            self.mydb = create_engine(
                f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            )

            # Test connection and list available tables
            with self.mydb.connect() as connection:
                print("Connection established successfully.")
                inspector = inspect(self.mydb)
                table_names = inspector.get_table_names()
                print("Tables in the database:\n*", "\n* ".join(table_names))
        except Exception as error:
            # Handle connection errors
            print("Error: Unable to connect to the MySQL database.")
            print(f"Error Details: {error}")
            self.mydb = None  # Ensure connection is None if failed


class AnalyseCSV:
    def __init__(self, urls):
        # Unpack the provided URLs
        self.go_daily_sales_URL, self.go_products_URL = urls

        # Initialise empty attributes (`self.go_daily_sales`, `self.go_products`, `self.merged_df`) to store the dataframes.
        self.go_daily_sales = None
        self.go_products = None
        self.merged_df = None

        # Call the `getCSVFiles` method to load and analyse the CSV files.
        self.getCSVFiles()
        # Call the `MergeDataFrame` method to merge the two datasets ('go_daily_sales' and 'go_products') into a single dataframe (`self.merged_df`) for further analysis.
        self.MergeDataFrame()


    def getCSVFiles(self):
        # Print a message to indicate which tables (CSV files) are being used.
        print("\n\nUsing tables:\ngo_daily_sales\ngo_products")

        # Call the `preformEDA` method for 'go_daily_sales' to load and analyse the daily sales CSV file.
        # Call the `preformEDA` method for 'go_products' to load and analyse the products CSV file.
        self.performEDA("go_daily_sales", self.go_daily_sales_URL)
        self.performEDA("go_products", self.go_products_URL)
        """       
        Each CSV file is analysed for its structure and content, and the results are stored 
        in the corresponding class attributes (`self.go_daily_sales` and `self.go_products`).
        The data analysis includes printing info about the dataframe, unique values, and displaying the first and last rows.

        This function ensures that both CSV files are loaded and ready for further data analysis tasks.
        """


    def performEDA(self, tablenme, url):
        print("\nEDA Output")
        try:
            # Load the CSV file into a pandas dataframe using the provided URL.
            frame = pd.read_csv(url)
            # Print a separator and the name of the table to clearly distinguish the output in the console.
            print(f"{'-'*50}\nTable name: {tablenme}")

            # Print the dataframe's structure and metadata using .info() to display column names, data types, and memory usage.
            print(frame.info())

            # Print the number of unique items in each column using .nunique() to show how many distinct values each column contains.
            print(f"\n\nUnique Items in Each Column for table {tablenme}:")
            print(frame.nunique())

            print(f"\n\nUnique Items in Each Column for table {tablenme}:")
            # Apply the .unique() function to print the unique values in each column, helping to identify patterns or outliers.
            print(frame.apply(pd.unique))

            # Display the first and last few rows of the dataframe for a quick visual snapshot using tabulate for nicely formatted output.
            print(tabulate(frame.head(), headers='keys', tablefmt='pretty')) # first rows
            print(tabulate(frame.tail(), headers='keys', tablefmt='pretty')) # last rows

            # Store the dataframe in the appropriate attribute based on the table name:
            if tablenme == 'go_daily_sales':
                self.go_daily_sales = frame
            else:
                self.go_products = frame

        except Exception as error:
            print(f"Error during EDA on table: {tablenme}: {error}")

        """
        This function performs Exploratory Data Analysis (EDA) on a CSV file loaded from the provided URL.
        It provides insights into the dataset by printing key information about its structure and content.

        This function helps provide a quick overview of the dataset for further analysis.
        """

    def MergeDataFrame(self):
        print("\n\nMerged Dataframe")


        # Extract relevant columns from the products dataframe ('Product number', 'Product', 'Unit cost').
        relevant_columns = self.go_products[['Product number', 'Product', 'Unit cost']]

       # print("Is 'Product number' in self.go_daily_sales:", 'Product number' in self.go_daily_sales.columns)
       # print("Is 'Product number' in go_products:", 'Product number' in self.go_products.columns)

        # Merge the dataframes, assuming 'Product number' is a common key
        try:
            # Merge the products dataframe with the daily sales dataframe based on 'Product number', using an inner join to include only matching rows.
            self.merged_df = pd.merge(self.go_daily_sales, relevant_columns, on='Product number', how='inner')
            print("Datasets merged successfully.")


            # Calculate additional columns:
            # 'Total Sales' by multiplying 'Quantity' with 'Unit sale price'.
            self.merged_df['Total Sales'] = self.merged_df['Quantity'] * self.merged_df['Unit sale price']

            # 'Total Profit' by subtracting the total cost (unit cost * quantity) from total sales.
            self.merged_df['Total Profit'] = self.merged_df['Unit cost'] * self.merged_df['Quantity']

            # Round the sales and profit values to two decimal places for clarity.
            self.merged_df['Total Sales'] = self.merged_df['Total Sales'].round(2)
            self.merged_df['Total Profit'] = self.merged_df['Total Profit'].round(2)

            # Print the first and last rows of the merged dataframe using the printDF function for inspection.
            self.printDF(self.merged_df.head(1))  # first row
            self.printDF(self.merged_df.tail(1))  # last row

        except KeyError as error:
            print("Error during merge: {error}")

        """
        This function merges two dataframes: one containing product information (from go_products) and 
        another containing daily sales data (from go_daily_sales). The merge is done based on the 
        'Product number' column, creating a comprehensive dataset for further analysis.

        This merged dataframe ('self.merged_df') becomes the central dataset used for further analysis,
        such as computing total sales, profit, and quantities sold by product.
        """

    def analyseTop10QuantitySales(self):
        print("Analyse Top 10 Quantity Sales")

        try:
            # Group the merged dataframe by 'Product' to aggregate values
            agg_product = self.merged_df.groupby('Product').agg(
                Total_Sales=('Total Sales', 'sum'),
                Total_Quantity_Sold=('Quantity', 'sum'),
                Total_Profit=('Total Profit', 'sum')
            ).reset_index()

            print("Aggregated Product Data:\n", agg_product)  # Debugging: Print aggregated results

            # Sort the products to find the top 10 products based on their total sales
            top_products = agg_product.sort_values(by='Total_Sales', ascending=False).head(10)
            print("Top 10 products by sales:\n", top_products)

            # Display the top 10 products in a formatted table with their respective sales and profit values
            print(tabulate(top_products, headers='keys', tablefmt='pretty'))

            # Create a bar chart to visualize the total sales and total profit for these top 10 products
            plt.figure(figsize=(12, 6))
            bar_width = 0.35
            index = np.arange(len(top_products))

            # Plot the Total Sales
            plt.bar(index, top_products['Total_Sales'], bar_width, label='Total Sales', color='b')

            # Plot the Total Profit stacked on top of Total Sales
            plt.bar(index, top_products['Total_Profit'], bar_width, label='Total Profit', color='g', bottom=top_products['Total_Sales'])

            # Adding labels and title
            plt.xlabel('Products')
            plt.ylabel('Amount')
            plt.title('Total Sales and Total Profit for Top 10 Products')
            plt.xticks(index, top_products['Product'], rotation=45, ha='right')
            plt.legend()

            # Show the plot
            plt.tight_layout()
            plt.show()

            # Display results in a Tkinter window with two bar charts (one for sales and one for profit)
            root = tk.Tk()

            # Create a new Toplevel window for the plots
            plot_window = tk.Toplevel(root)
            plot_window.title("Top 10 Products: Sales and Profit (Stacked)")

            # Create a figure and axis for the stacked bar chart
            fig = Figure(figsize=(10, 6), dpi=100)
            ax_sales = fig.add_subplot(111)  # Single subplot for stacked sales and profit

            # Prepare labels with wrapped text to improve readability on x-axis
            wrapped_labels = [textwrap.fill(product, width=10) for product in top_products['Product']]

            # Plot the Total Sales as the base of each bar
            ax_sales.bar(top_products['Product'], top_products['Total_Sales'], color='b', label='Total Sales')

            # Stack Total Profit on top of Total Sales
            ax_sales.bar(top_products['Product'], top_products['Total_Profit'], bottom=top_products['Total_Sales'],
                         color='g', label='Total Profit')

            # Set labels, title, and legend
            ax_sales.set_xlabel('Products')
            ax_sales.set_ylabel('Amount')
            ax_sales.set_title('Total Sales and Profit for Top 10 Products (Stacked)')
            ax_sales.set_xticks(range(len(wrapped_labels)))
            ax_sales.set_xticklabels(wrapped_labels, rotation=45, ha='right')
            ax_sales.legend()

            # Use a Tkinter canvas to show the plot with a toolbar for interaction
            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            # Toolbar for interaction
            toolbar = NavigationToolbar2Tk(canvas, plot_window)
            toolbar.update()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            # Add a button to close the window
            button_close = tk.Button(plot_window, text="Close", command=plot_window.destroy)
            button_close.pack()

            # Start the Tkinter main loop
            root.mainloop()

        except Exception as error:
            print(f"Error during analysis of top 10 products by quantity sales: {error}")

        """
        This function analyses the top 10 products based on total sales from the dataset.

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
