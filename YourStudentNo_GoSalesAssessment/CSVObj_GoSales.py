import pandas as pd
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from tabulate import tabulate
from sqlalchemy import create_engine, inspect
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import textwrap

"""
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
"""

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


    """       
    Each CSV file is analysed for its structure and content, and the results are stored 
    in the corresponding class attributes (`self.go_daily_sales` and `self.go_products`).
    The data analysis includes printing info about the dataframe, unique values, and displaying the first and last rows.

    This function ensures that both CSV files are loaded and ready for further data analysis tasks.
    """
    def getCSVFiles(self):
        # Print a message to indicate which tables (CSV files) are being used.
        print("\n\nUsing tables:\ngo_daily_sales\ngo_products")

        # Call the `preformEDA` method for 'go_daily_sales' to load and analyse the daily sales CSV file.
        # Call the `preformEDA` method for 'go_products' to load and analyse the products CSV file.
        self.performEDA("go_daily_sales", self.go_daily_sales_URL)
        self.performEDA("go_products", self.go_products_URL)


    """
    This function performs Exploratory Data Analysis (EDA) on a CSV file loaded from the provided URL.
    It provides insights into the dataset by printing key information about its structure and content.

    This function helps provide a quick overview of the dataset for further analysis.
    """
    def performEDA(self, tablenme, url):
        print("\nEDA Output")
        try:
            # Load the CSV file into a pandas dataframe using the provided URL.
            frame = pd.read_csv(url)
            # Print a separator and the name of the table to clearly distinguish the output in the console.
            print(f"{'-'*50}\nTable name: {tablenme}")

            # Print the dataframe's structure and metadata using .info() to display column names, data types, and memory usage.
            print('\nPrint DataFrame Info for table: {0}'.format(tablenme))
            print(frame.info())

            # Print the number of unique items in each column using .nunique() to show how many distinct values each column contains.
            print(f"\n\nNumber of Unique Items in Each Column for table {tablenme}:")
            print(frame.nunique())

            print(f"\n\nUnique Items in Each Column for table {tablenme}:")
            # Apply the .unique() function to print the unique values in each column, helping to identify patterns or outliers.
            print(frame.apply(pd.unique))

            # Display the first and last few rows of the dataframe for a quick visual snapshot using tabulate for nicely formatted output.
            print(f"Table: {tablenme}")
            print(tabulate(frame.head(), headers='keys', tablefmt='pretty', showindex=True)) # first rows
            print(tabulate(frame.tail(), headers='keys', tablefmt='pretty', showindex=True)) # last rows

            # Store the dataframe in the appropriate attribute based on the table name:
            if tablenme == 'go_daily_sales':
                self.go_daily_sales = frame.copy()
            else:
                self.go_products = frame.copy()

        except Exception as error:
            print(f"Error during EDA on table: {tablenme}: {error}")


        """
        This function merges two dataframes: one containing product information (from go_products) and 
        another containing daily sales data (from go_daily_sales). The merge is done based on the 
        'Product number' column, creating a comprehensive dataset for further analysis.

        This merged dataframe ('self.merged_df') becomes the central dataset used for further analysis,
        such as computing total sales, profit, and quantities sold by product.
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
            self.merged_df = pd.merge(relevant_columns, self.go_daily_sales[['Product number', 'Date', 'Quantity', 'Unit price', 'Unit sale price']],
                                      on='Product number', how='inner')
            print("Datasets merged successfully.")

            # Calculate additional columns:
            # 'Total Sales' by multiplying 'Quantity' with 'Unit sale price'.
            self.merged_df['Total Sales'] = self.merged_df['Quantity'] * self.merged_df['Unit sale price']

            # 'Total Profit' by subtracting the total cost (unit cost * quantity) from total sales.
            self.merged_df['Total Profit'] = self.merged_df['Total Sales'] - (self.merged_df['Unit cost'] * self.merged_df['Quantity'])

            # Round the sales and profit values to two decimal places for clarity.
            self.merged_df['Total Sales'] = self.merged_df['Total Sales'].round(2)
            self.merged_df['Total Profit'] = self.merged_df['Total Profit'].round(2)

            # Print
            self.printDF(self.merged_df)
            # Print the first and last rows of the merged dataframe using the printDF function for inspection.
            #self.printDF((self.merged_df).head(1))  # first row
            #self.printDF((self.merged_df).tail(1))  # last row

        except KeyError as error:
            print("Error during merge: {error}")


    """
    This function analyses the top 10 products based on total sales from the dataset.
    The output includes both a printed table of the top 10 products and a visual plot that 
    helps compare their sales and profit.
    """
    def analyseTop10QuantitySales(self):
        print("Analyse Top 10 Quantity Sales")

        product_sums = self.merged_df.groupby('Product').agg({'Product number': 'count', 'Unit price': 'first',
        'Quantity': 'sum', 'Total Sales': 'sum', 'Total Profit': 'sum'}).reset_index()

        resultset = product_sums.nlargest(n=10, columns=['Total Sales']).sort_values('Total Sales', ascending=False)

        print(tabulate(product_sums.nlargest(n=10, columns=['Total Sales']), headers=['Product', 'No of Sales', 'Unit Price', 'Quantity Sold',
        'Total Sales', 'Total Profit'], floatfmt=".2f"))

        # wrapping text for x-labels
        wrapped_labels = [textwrap.fill(label, 10) for label in resultset['Product']]

        # create the main window
        root = tk.Tk()
        root.title("Top 10 Products")

        # create a custom frame to hold the Matplotlib plot
        frame = ttk.Frame(root)
        frame.pack(expand=True, fill=tk.BOTH)

        # create Matplotlib figure and subplot
        fig, ax = plt.subplots(figsize=(12,8))

        # modify the x and y labels on the axis to ensure nonscientific notation (i.e. no '1e6')
        # text is wrapped where too long
        ax.ticklabel_format(axis='y', style='plain')
        ax.set_xticks(range(len(wrapped_labels)))
        ax.set_xticklabels(wrapped_labels)

        # Plot the two bar charts for the total sales and total product
        # Set the colour for each
        # Set the bottom chart to be the Total Sales as it is higher value
        # Add the product label to the x-axis
        # Add the Amount in € to the y-axis
        # Set the title of the chart to be Top 10 Products based on Sales and Profit
        # Include Legend
        ax.bar(resultset['Product'], resultset['Total Sales'], label='Total Sales', color='red')
        ax.bar(resultset['Product'], resultset['Total Sales'], label='Total Sales', color='blue', bottom=resultset['Total Sales'])
        ax.set_xlabel('Product')
        ax.set_ylabel('Amount in €')
        ax.set_title('Top 10 Product based on Sales and Profit')
        ax.legend()

        # create a Matplotlib canvas within the frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # add a toolbar
        toolbar = NavigationToolbar2Tk(canvas, frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        toolbar.update()

        # start the Tkinter main loop
        root.mainloop()


    """
    This function analyses the sales data for a specific product based on the provided product ID (prod_ID).
    It filters the data for that product, calculates relevant statistics such as total sales, profit, and the 
    number of orders. Additionally, it visualises the total sales and profit, and plots the number of orders 
    per year using a bar chart.
    """
    def analyseProductByID(self, prod_ID):
        print("Analyse Product by ID")

        # Filter the dataframe for the product with the given product ID.
        result = self.merged_df[self.merged_df['Product number'] == prod_ID]
        orders = result[['Date', 'Quantity', 'Unit sale price', 'Total Sales', 'Total Profit']].copy()
        filtered = orders[orders['Unit sale price'] != 0]

        # Compute statistics like total quantity sold, total sales, total profit, and number of orders.
        print("Product Info based on ID: {0}\t{1}".format(prod_ID, result['Product'].iat[0]))
        unitPrice = result['Unit price'].iat[0]
        unitCost = result['Unit cost'].iat[0]
        total_sold = filtered["Quantity"].sum()
        total_sales = filtered['Total Sales'].sum()
        total_profit = filtered['Total Profit'].sum()
        totalNoOrders = len(filtered)

        print('Unit Price: €{0}'.format(unitPrice))
        print('Unit cost: €{0}'.format(unitCost))
        print('Totals:\nOrders: {0}'.format(totalNoOrders))
        print(f"Total Quantity Sold: {total_sold}")
        print(f"Sales: €{round(total_sales,2)}")
        print(f"Profit: €{round(total_profit,2)}")
        tabulate(tabulate(filtered, headers='keys', tablefmt='pretty', showindex=True))

        # Convert the 'Date' column to datetime
        orders['Date'] = pd.to_datetime(orders['Date'], dayfirst=True)
        # Group by year
        orders['Year'] = orders['Date'].dt.year
        orders_per_year = orders.groupby('Year')['Quantity'].sum()

        # Create the main window
        root = tk.Tk()
        root.title("Go Sales")

        # Create a Tkinter window to show the charts.
        frame = ttk.Frame(root)
        frame.pack(expand=True, fill=tk.BOTH)

        # Create a Matplotlib figure and subplot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8), dpi=100)
        ax1.ticklabel_format(axis='y', style='plain')

        ax1.bar('Total Sales', total_sales, label='Total Sales', color='red')
        ax1.bar('Total Profit', total_profit, label='Total Profit', color='blue')
        ax1.set_xlabel('Sales')
        ax1.set_ylabel('Amount in €')
        ax1.set_title('Product: {0} ({1})'.format(result['Product'].iat[0], prod_ID))
        ax1.legend()

        # Plot the total orders per year on a line chart.
        # Plot the orders per year with x-ticks formatted to show years
        ax2.plot(orders_per_year.index, orders_per_year.values, marker='o', linestyle='-')
        ax2.tick_params(axis='x', rotation=45)
        ax2.set_title('Total Orders per Year')
        ax2.set_xlabel('Year')
        ax2.set_ylabel('Total Orders')

        # Create a Matplotlib canvas within the frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Add a toolbar
        toolbar = NavigationToolbar2Tk(canvas, frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        toolbar.update()

        # Start the Tkinter main loop
        root.mainloop()

    """ 
    This function prints the first and last few rows of a given dataframe in a nicely formatted way.
    It uses the `tabulate` library to format the output, making it easier to read.
    This function provides a quick overview of the content of the dataframe, ensuring that both the start and end of the data can be easily inspected.
    """
    def printDF(self, dataframe):
        # Display the first and last five rows of the DataFrame
        print(tabulate(dataframe.head(), headers='keys', tablefmt='pretty', showindex=True))
        print(tabulate(dataframe.tail(), headers='keys', tablefmt='pretty', showindex=True))
        print("\n")






