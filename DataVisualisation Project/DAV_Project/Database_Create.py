import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, inspect
from tabulate import tabulate
import re


class DBConnection_Alchemy:
    def __init__(self, connect_info):
        # Unpack connection details and set up database configuration
        self.host, self.user, self.password, self.port, self.database = connect_info
        self.mydb = None
        self.connectNow()  # Initialize database connection

    def connectNow(self):
        print(
            f"Attempting to connect using:\nHost: {self.host}\nUser: {self.user}\nPort: {self.port}\nDatabase: {self.database}"
        )
        try:
            self.mydb = create_engine(
                f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            )
            # Test connection
            with self.mydb.connect() as connection:
                print("Connection established successfully.")
                inspector = inspect(self.mydb)

        except Exception as error:
            print("Error: Unable to connect to the MySQL database.")
            print(f"Error Details: {error}")
            self.mydb = None

    def visualiseGenderDistribution(self):
        # Validate connection before visualizing client data
        if self.mydb is None:
            print("Error: Database connection not established.")
            return

        try:
            frame = pd.read_sql("SELECT * FROM actors", self.mydb)
            pd.set_option('display.expand_frame_repr', False)
            gender_counts = frame['sex'].value_counts(dropna=False)
            plt.pie(gender_counts, labels=gender_counts.index, autopct='%.1f%%')
            plt.legend(gender_counts.index)
            plt.title("Actors - Gender Distribution")
            plt.show()
        except Exception as error:
            print(f"Error while visualizing client data: {error}")

    def disposeConnection(self):
        if self.mydb:
            self.mydb.dispose()
            print("Database connection closed.")
