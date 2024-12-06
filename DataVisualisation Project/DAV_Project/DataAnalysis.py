import pandas as pd
from sqlalchemy import inspect
from tabulate import tabulate
import io

class DataAnalysis:
    def __init__(self, connection, log_function=None):
        self.connection = connection
        self.table = ""
        self.log_function = log_function or (lambda msg: print(msg))
        self.connectNow()


    def connectNow(self):
        inspector = inspect(self.connection)
        table_names = inspector.get_table_names()
        self.log_function("Tables in the database:\n* " + "\n* ".join(table_names))


    # Load data, perform exploratory data analysis (EDA)
    def performEDA(self):
        if self.connection is None:
            self.log_function("Error: Database connection not established.")
            return
        if not self.table:
            self.log_function("Error: No table selected for EDA.")
            return

        try:
            # Load data
            frame = pd.read_sql(f"SELECT * FROM {self.table}", self.connection)

            # Redirect output of frame.info() to a string buffer
            buffer = io.StringIO()
            frame.info(buf=buffer)
            info_str = buffer.getvalue()

            # Log EDA results
            self.log_function(f"DataFrame Info for table {self.table}:\n{info_str}")
            self.log_function(f"Number of Unique Items in {self.table}:\n{frame.nunique()}")
            self.log_function(f"Unique Items in Each Column for table {self.table}:\n{frame.apply(pd.unique)}")

            # Table preview
            self.log_function("Table Preview (First 10 rows):\n")
            self.log_function(tabulate(frame.head(10), headers='keys', tablefmt='pretty', showindex=True))
            self.log_function("\nTable Preview (Last 10 rows):\n")
            self.log_function(tabulate(frame.tail(10), headers='keys', tablefmt='pretty', showindex=True))

        except Exception as error:
            self.log_function(f"Error during EDA on table '{self.table}': {error}")

    # Set table for analysis and trigger EDA
    def selectTable(self, table_name):
        try:
            self.table = table_name
            self.log_function(f"Selecting table '{table_name}' for analysis.")
            self.performEDA()
        except Exception as e:
            self.log_function(f"Error selecting table '{table_name}': {e}")


    def printDF(self, dataframe):
        # Display the first and last ten rows of the DataFrame
        self.log_function(tabulate(dataframe.head(10), headers='keys', tablefmt='pretty', showindex=True))
        self.log_function(tabulate(dataframe.tail(10), headers='keys', tablefmt='pretty', showindex=True))
        self.log_function("\n")
