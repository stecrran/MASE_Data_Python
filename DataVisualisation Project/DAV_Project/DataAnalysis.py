import pandas as pd
from sqlalchemy import create_engine, inspect
import matplotlib.pyplot as plt
from tabulate import tabulate

class DataAnalysis:
    def __init__(self, connection):
        self.connection = connection
        self.table = ""
        #self.connectNow()


    def connectNow(self):
        inspector = inspect(self.connection)
        table_names = inspector.get_table_names()
        print("Tables in the database:\n*", "\n* ".join(table_names))


    def performEDA(self):
        # Validate connection and table selection
        if self.connection is None:
            print("Error: Database connection not established.")
            return
        if not self.table:
            print("Error: No table selected for EDA.")
            return

        # Load data and perform exploratory data analysis (EDA)
        try:
            frame = pd.read_sql(f"SELECT * FROM {self.table}", self.connection)
            pd.set_option('display.expand_frame_repr', False)
            print(f"\n\nDataFrame Info for table {self.table}:")
            print(frame.info())
            print(f"\n\nNumber of Unique Items in {self.table}:")
            print(frame.nunique())
            print(f"\n\nUnique Items in Each Column for table {self.table}:")
            print(frame.apply(pd.unique))
            print("\n\nTable Preview:")
            self.printDF(frame)
        except Exception as error:
            print(f"Error during EDA on table '{self.table}': {error}")


    def selectTable(self, table_name):
        # Set the table for analysis and trigger EDA
        print(f"Selecting table '{table_name}' for analysis.")
        self.table = table_name
        self.performEDA()


    def printDF(self, dataframe):
        # Display the first and last ten rows of the DataFrame
        print(tabulate(dataframe.head(10), headers='keys', tablefmt='pretty', showindex=True))
        print(tabulate(dataframe.tail(10), headers='keys', tablefmt='pretty', showindex=True))
        print("\n")