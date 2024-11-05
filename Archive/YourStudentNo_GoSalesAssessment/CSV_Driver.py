from matplotlib.pyplot import table

from CSVObj_GoSales import AnalyseCSV
from CSVObj_GoSales import DBConnection_Alchemy


# This function orchestrates the loading, analysing, and displaying of sales and product data.
def main():

    print("Getting CSV files from server")
    host = "db.relational-data.org"
    user = "guest"
    password = "relational"
    port = 3306
    database = "GOSales"


    # create tuple to store all this information IF using remote database
    db_info = (host, user, password, port, database)
    # pass the tuple to the DBConnecction class
    relationalDB = DBConnection_Alchemy(db_info)


    # Define the URLs for two CSV files:
    go_daily_sales_URL = "https://davmase.z6.web.core.windows.net/GoSales/go_daily_sales.csv"
    go_products_URL = "https://davmase.z6.web.core.windows.net/GoSales/go_products.csv"

    # Pack these URLs into a tuple (`csvFiles`) to pass them as a single argument.
    csvFiles = (go_daily_sales_URL, go_products_URL)

    # Create an instance of the `AnalyseCSV` class, passing the `csvFiles` tuple, which loads and merges the data.
    analysis = AnalyseCSV(csvFiles)

    # Call methods from the `AnalyseCSV` instance:
    # `analyseTop10QuantitySales()` to analyse and display the top 10 products by sales.
    analysis.analyseTop10QuantitySales()

    # `analyseProductByID(5110)` to analyse sales data for the product with ID 5110.
    analysis.analyseProductByID(5110)

    # Print a message indicating the closure of the connection, signaling that the tasks have completed.
    print("Connection closed")

if __name__ == '__main__':
    main()