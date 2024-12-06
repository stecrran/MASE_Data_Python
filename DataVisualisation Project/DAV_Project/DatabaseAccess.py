from sqlalchemy import create_engine, inspect

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



    def disposeConnection(self):
        if self.mydb:
            self.mydb.dispose()
            print("Database connection closed.")
