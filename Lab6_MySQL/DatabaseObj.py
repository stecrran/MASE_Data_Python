import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, inspect
from tabulate import tabulate

class DBConnection:
    def __init__(self, connect_info):
        # Unpack connection details and set up database configuration
        self.host, self.user, self.password, self.port, self.database = connect_info
        self.table = ""
        self.mydb = None
        self.connectNow()  # Initialize database connection

    def connectNow(self):
        # Print connection details for debugging (avoid in production)
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
                print("Tables in the database:", ", ".join(table_names))
        except Exception as error:
            # Handle connection errors
            print("Error: Unable to connect to the MySQL database.")
            print(f"Error Details: {error}")
            self.mydb = None  # Ensure connection is None if failed

    def performEDA(self):
        # Validate connection and table selection
        if self.mydb is None:
            print("Error: Database connection not established.")
            return
        if not self.table:
            print("Error: No table selected for EDA.")
            return

        # Load data and perform exploratory data analysis (EDA)
        try:
            frame = pd.read_sql(f"SELECT * FROM {self.table}", self.mydb)
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

    def visualiseClient(self):
        # Validate connection before visualizing client data
        if self.mydb is None:
            print("Error: Database connection not established.")
            return

        try:
            frame = pd.read_sql("SELECT * FROM client", self.mydb)
            pd.set_option('display.expand_frame_repr', False)
            gender_counts = frame['gender'].value_counts(dropna=False)
            plt.pie(gender_counts, labels=gender_counts.index, autopct='%.1f%%')
            plt.legend(gender_counts.index)
            plt.title("Client Gender Distribution")
            plt.show()
        except Exception as error:
            print(f"Error while visualizing client data: {error}")

    def selectTable(self, table_name):
        # Set the table for analysis and trigger EDA
        print(f"Selecting table '{table_name}' for analysis.")
        self.table = table_name
        self.performEDA()

    def printDF(self, dataframe):
        # Display the first and last five rows of the DataFrame
        print(tabulate(dataframe.head(), headers='keys', tablefmt='pretty', showindex=True))
        print(tabulate(dataframe.tail(), headers='keys', tablefmt='pretty', showindex=True))
        print("\n")

    def disposeConnection(self):
        # Safely close the database connection
        if self.mydb:
            self.mydb.dispose()
            print("Database connection closed.")
