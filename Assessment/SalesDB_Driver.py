from SalesDB_Obj import SalesDB

def main():
    # Load data from URLs (replace 'url' with actual file paths if needed)
    # This will speed up time when running the files locally

    customers = "C:/Users/A00325351/Desktop/assessment/Date Difference Demo-20241106/Customers.csv"
    employees = "C:/Users/A00325351/Desktop/assessment/Date Difference Demo-20241106/Employees.csv"
    products = "C:/Users/A00325351/Desktop/assessment/Date Difference Demo-20241106/Products.csv"
    sales = "C:/Users/A00325351/Desktop/assessment/Date Difference Demo-20241106/Sales.csv"

    """
    customers = "https://davmase.z6.web.core.windows.net/salesDB/Customers.csv"
    employees = "https://davmase.z6.web.core.windows.net/salesDB/Employees.csv"
    products = "https://davmase.z6.web.core.windows.net/salesDB/Products.csv"
    sales = "https://davmase.z6.web.core.windows.net/salesDB/Sales.csv"
    """

    csvFiles = (customers, employees, products, sales)

    # Instantiate SalesDB
    sales_db = SalesDB(csvFiles)

    # Call each function as per assignment requirements
    sales_db.analyseTop10()
    sales_db.sales_by_month(60, 2020)
    sales_db.deliveryDispatchAnalysis()


if __name__ == "__main__":
    main()


