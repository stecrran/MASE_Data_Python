import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate


class SalesDB:
    def __init__(self, urls):
        self.customers_URL, self.employees_URL, self.products_URL, self.sales_URL = urls
        # Create empty dataframes for each table and the merged dataframe
        self.customers = None
        self.employees = None
        self.products = None
        self.sales = None
        self.merged_df = None
        # Once the dataframes have been unpacked, call the getConnectionProgress and MergeDataFrame functions
        self.getConnectionProgress()
        self.MergeDataFrame()


    def getConnectionProgress(self):
        print("Getting Connection Progress...")
        self.preformEDA('customers', self.customers_URL)
        self.preformEDA('employees', self.employees_URL)
        self.preformEDA('products', self.products_URL)
        self.preformEDA('sales', self.sales_URL)


    def preformEDA(self, tablenme, url):
        print("Preforming EDA...")
        # Loads data from the provided `url` into a dataframe for analysis.
        frame = pd.read_csv(url)

        print(f"\n{'*' * 20}\t{ tablenme }\t{'*' * 20}")
        # Prints a header to visually separate output for each table in the console.
        # Displays basic information about the dataframe, including columns, data types, and memory usage.
        print('\nPrint DataFrame Info for table: {0}'.format(tablenme))
        print(frame.info())

        # Prints the number of unique items in each column to identify distinct records.
        print(f"\n\nNumber of Unique Items in Each Column for table {tablenme}:")
        print(frame.nunique())

        # Displays unique values for each column to identify potential data inconsistencies or outliers.
        print(f"\n\nUnique Items in Each Column for table {tablenme}:")
        # Apply the .unique() function to print the unique values in each column, helping to identify patterns or outliers.
        print(frame.apply(pd.unique))


        # Uses the `tabulate` library to print the first and last few rows of the dataframe in a formatted table.
        print(f"Table: {tablenme}")
        print(tabulate(frame.head(), headers='keys', tablefmt='pretty', showindex=True))  # first rows
        print(tabulate(frame.tail(), headers='keys', tablefmt='pretty', showindex=True))  # last rows

        # Checks the table name (`tablenme`) to assign the loaded dataframe to the corresponding attribute:
        # - If `Customers`, it copies the dataframe to `self.customers`.
        # - If `Employees`, it copies the dataframe to `self.employees`.
        # - If `Products`, it copies the dataframe to `self.products`.
        # - Otherwise, it copies the dataframe to `self.sales`.
        if tablenme == 'customers':
            self.customers = frame.copy()
        elif tablenme == 'employees':
            self.employees = frame.copy()
        elif tablenme == 'products':
            self.products = frame.copy()
        else:
            self.sales = frame.copy()




    def MergeDataFrame(self):
        print("Merging")
        # Merges `self.sales` and `self.products` on a common column, `ProductID`, using an inner join.
        self.merged_df = pd.merge(self.sales, self.products, on='ProductID', how='inner')
        print("Datasets merged successfully.")

        # Replaces any `0` prices in the merged dataframe with `0.05` to avoid issues with free products.
        self.merged_df['Price'] = self.merged_df['Price'].replace('0', '0.05')

        # Calculates `TotalSales` by multiplying `Quantity` and `Price` columns and rounds the result to 2 decimals.
        self.merged_df['Total Sales'] = self.merged_df['Quantity'] * self.merged_df['Price'].round(2)

        # Calculates a `Vat` column as a small percentage of `TotalSales` and rounds to 2 decimals.
        self.merged_df['Vat'] = self.merged_df['Total Sales'] * 0.013
        self.merged_df['Vat'] = self.merged_df['Vat'].round(2)

        # Calculates `TotalIncVat` by adding `Vat` to `TotalSales` for a final sales value.
        self.merged_df['TotalIncVat'] = (self.merged_df['Total Sales'] + self.merged_df['Vat']).round(2)

        # Converts `OrderDate` and `DispatchDate` columns to datetime objects in a specified format.
        self.merged_df['OrderDate'] = pd.to_datetime(self.merged_df['OrderDate'], format='%d-%m-%Y', errors='coerce')
        self.merged_df['DispatchDate'] = pd.to_datetime(self.merged_df['DispatchDate'], format='%d-%m-%Y', errors='coerce')

        # Calculates the difference between `DispatchDate` and `OrderDate` in days, storing it in a new column `DateDifference`.
        self.merged_df['DateDifference'] = (self.merged_df['DispatchDate'] - self.merged_df['OrderDate']).dt.days

        # Optionally saves the merged dataframe as a CSV file called "Merged.csv" for external use.
        #self.merged_df.to_csv("Merged.csv", index=False)

        # Prints the first few rows of the merged dataframe to the console using the `tabulate` library.
        print(f"\n\n\n{'*' * 20}\tMerged Dataframe\t{'*' * 20}")
        print(tabulate(self.merged_df.head(10), headers='keys', tablefmt='grid'))



    def analyseTop10(self):
        print("Analysing")
        # Groups data in `merged_df` by product name and calculates the total sales, selecting the top 10 products.
        top_products = self.merged_df.groupby('Name')['Total Sales'].sum().nlargest(10).reset_index()

        # Displays the top 10 selling products in a formatted table.
        print("\nTop 10 Selling Products:")
        print(tabulate(top_products[['Name', 'Total Sales']], headers='keys', tablefmt='grid'))

        # Creates a subplot with two sections for pie charts: top products and top customers.
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8))

        # Combines customer names into a full name field in the `customers` dataframe.
        self.customers['Full Name'] = self.customers['FirstName'] + ' ' + self.customers['LastName']

        top_customers = self.merged_df.groupby('CustomerID')['Total Sales'].sum().nlargest(10).reset_index()
        # Merges `top_customers` with the `customers` dataframe to add customer names to the top customer sales data.me'
        top_customers = top_customers.merge(self.customers[['CustomerID', 'Full Name']], on='CustomerID', how='left')

        # Prints a table of the top 10 customers by total sales.
        print("\nTop 10 Customers by Sales:")
        # Print 'CustomerID', 'Full Name', and 'Total Sales' using tabulate
        print(tabulate(top_customers[['CustomerID', 'Full Name', 'Total Sales']], headers='keys', tablefmt='grid'))

        labels1 = top_products['Name']
        sizes1 = top_products['Total Sales']

        labels2 = top_customers['Full Name']
        sizes2 = top_customers['Total Sales']

        # Generates a pie chart for the top 10 products by total sales, with labels showing percentages.
        ax1.pie(sizes1, labels=labels1, autopct='%1.1f%%', startangle=140)
        ax1.set_title("Top 10 Selling Products")

        # Generates a pie chart for the top 10 products by total sales, with labels showing percentages.
        ax2.pie(sizes2, labels=labels2, autopct='%1.1f%%', startangle=140)
        ax2.set_title("Top 10 Customers by Sales")
        plt.show()

        # Generates a pie chart for the top 10 customers by total sales, with labels showing percentages.
        # Displays the generated pie charts.

    def sales_by_month(self, product_id, year):
        print("Sales by month")
        # Filters `merged_df` for the specified `product_id` and `year`.
        filtered_df = self.merged_df.filter(items=[product_id, year])

        filtered_df = self.merged_df[(self.merged_df['ProductID'] == product_id) & (self.merged_df['OrderDate'].dt.year == year)].copy()

        # Group the filtered data by month, calculating total sales for each month
        monthly_sales = filtered_df.groupby(filtered_df['OrderDate'].dt.to_period('M'))['Total Sales'].sum().reset_index()

        # Convert 'OrderDate' back to a timestamp format
        monthly_sales['OrderDate'] = monthly_sales['OrderDate'].dt.to_timestamp()

        # Renames columns for clarity in the output.
        monthly_sales.rename(columns={'OrderDate': 'Month'}, inplace=True)
        #print(monthly_sales)

        # Converts month numbers to abbreviated month names for readability.
        monthly_sales['Month'] = pd.to_datetime(monthly_sales['Month']) # Convert the 'Date' column to datetime

        # Converts the numberical 'Month' value to Month MMM string
        # monthly_sales['Month'] = monthly_sales['Month'].dt.strftime("%d %B %Y") # DD-MON-YYYY
        monthly_sales['Month'] = monthly_sales['Month'].dt.strftime("%B")
        print(monthly_sales)

        # Retrieves the name of the product using `product_id` from the `products` dataframe.
        result = self.products.loc[self.products['ProductID'] == product_id, 'Name'].values[0]

        # Calculates the total and average monthly sales, displaying these values with formatting.
        #print(f"Total monthly sales: {monthly_sales['Total Sales'].sum()}", f"\nAverage monthly sales: {monthly_sales['Total Sales'].mean()}")
        #print("Total monthly sales:", monthly_sales.groupby('Month')['Total Sales'].agg({'sum', 'mean'}).reset_index())

        # Group by 'Month' and calculate the sum and mean of 'Total Sales' for each month
        monthly_summary = monthly_sales.groupby('Month')['Total Sales'].agg(['sum', 'mean']).reset_index()

        # Calculate the overall total and average monthly sales
        total_sales = monthly_summary['sum'].sum()
        average_sales = monthly_summary['mean'].mean()

        print(f"Total monthly sales: {total_sales}", f"\nAverage monthly sales: {average_sales}")

        # Prints a breakdown of monthly sales data in a tabular format.
        print(tabulate(monthly_sales, headers='keys', tablefmt='grid'))

        # Plots a line chart of monthly sales with markers at each data point.
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(monthly_sales['Month'], monthly_sales["Total Sales"], marker='o', linestyle='-')
        ax.tick_params(axis='x', rotation=45)
        ax.set_title(f'Monthly Sales for Product ID {product_id} in {year}')
        ax.set_xlabel('Month')
        ax.set_ylabel('Total Sales')

        plt.grid()
        plt.show()


    def deliveryDispatchAnalysis(self):
        print("Delivery Dispatch")
        # Analyses dispatch times by categorising them into time ranges and calculating the average shipping days.
        # Calculates the average number of days between order and dispatch dates.
        # Categorises dispatch times into ranges: <7 days, 7-14 days, and 14-30 days.
        # Counts occurrences of each dispatch time category.
        # Prints the average shipping days and counts in each category in a formatted table.
        # Plots a bar chart of dispatch time categories with a line showing the average shipping days.
        # Displays the bar chart and average shipping days.
