import pandas as pd
from matplotlib.pyplot import table
from sqlalchemy import create_engine, inspect
from tabulate import tabulate
import sys
# imports for plotting:
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DBConnection_Alchemy:
    def __init__(self, connect_info):
        # Unpack connection details and set up database configuration
        self.host, self.user, self.password, self.port, self.database = connect_info
        self.table = ""
        self.mydb = None
        self.db_config = {
            'host': self.host,
            'user': self.user,
            'password' : self.password,
            'port' : self.port,
            'database': self.database
        }
        self.connectNow()  # Initialize database connection

    def connectNow(self):
        # Print the connection data to the user so they can see what was entered
        self.connectionProgress = "New Connection using:"\
            '\nhost: {0}'\
            '\nuser: {1}'\
            '\npassword : {2}'\
            '\nport : {3}'\
            '\ndatabase: {4}\n\n'.format(self.host, self.user, self.password, self.port, self.database)

        # Print connection details for debugging (avoid in production)
        # print(f"Attempting to connect using:\nHost: {self.host}\nUser: {self.user}\nPort: {self.port}\nDatabase: {self.database}")

        try:
            # Create SQLAlchemy engine to connect to the database
            self.mydb = create_engine(
                f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            )

            # Test connection and list available tables
            with self.mydb.connect() as connection:
                print("Connection established successfully.")
                # create an inspector object to inspect the database
                inspector = inspect(self.mydb)
                # get the list of table names in the database
                table_names = inspector.get_table_names()
                # print the list of table names
                # print("Tables in the database:\n*", "\n* ".join(table_names))
                self.connectionProgress += "Tables in the database:"
                for table_name in table_names:
                    self.connectionProgress += "\n"+table_name

        except Exception as error:
            # Handle connection errors
            print("Error: Unable to connect to the MySQL database.")
            print(f"Error Details: {error}")
            self.mydb = None  # Ensure connection is None if failed

    def getConnectionProgress(self):
        return self.connectionProgress

    def performEDA(self):
        # Validate connection and table selection
        if self.mydb is None:
            print("Error: Database connection not established.")
            return
        if not self.table:
            print("Error: No table selected for EDA.")
            return

        try:
            # Escape the table name with backticks
            frame = pd.read_sql(f"SELECT * FROM `{self.table}`", self.mydb)
            pd.set_option('display.expand_frame_repr', False)

            # Write detailed EDA output to a file
            with open('tableInfo.txt', 'w') as f:
                sys.stdout = f
                print(f"\n\nDataFrame Info for table {self.table}:")
                frame.info()
                print(f"\n\nNumber of Unique Items in {self.table}:")
                print(frame.nunique())
                print(f"\n\nUnique Items in Each Column for table {self.table}:")
                print(frame.apply(pd.unique))
                print("\n\nTable: {0}".format(self.table))
                print(tabulate(frame.head(), headers='keys', tablefmt='pretty', showindex=True))
                print(tabulate(frame.tail(), headers='keys', tablefmt='pretty', showindex=True))

        except Exception as error:
            print(f"Error during EDA on table '{self.table}': {error}")

        finally:
            # Reset stdout to console
            sys.stdout = sys.__stdout__

        print(f"EDA results saved to 'tableInfo.txt'.")

    def visualiseClient(self):
        frame = pd.read_sql(f"SELECT * FROM client", self.mydb);
        pd.set_option('display.expand_frame_repr', False)
        values = frame['gender'].value_counts(dropna=False)
        labels = frame['gender'].unique().tolist()

        # create the main window
        root = tk.Tk()
        root.title("Gender")

        # create a custom frame to hold the Matplotlib plot
        frame = ttk.Frame(root)
        frame.pack(expand=True, fill=tk.BOTH)

        # create a Matplotlib figure and subplot
        fig = Figure(figsize = (5,4), dpi=100)
        subplot = fig.add_subplot(111)
        subplot.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)

        # create a Matplotlib canvas within the frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # start the Tkinter main loop
        root.mainloop()

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
