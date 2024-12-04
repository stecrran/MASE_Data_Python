from AppGUI import AppGUI
from FetchData import FetchData
from ActorSearch import ActorSearch
from GenreSearch import GenreSearch
from VisualiseData import VisualiseData
from DataAnalysis import DataAnalysis
from DatabaseAccess import DBConnection_Alchemy
import tkinter as tk

def main():
    host = "db.relational-data.org"
    user = "guest"
    password = "relational"
    port = 3306
    database = "imdb_full"

    # Create tuple to store all this information
    db_info = (host, user, password, port, database)

    # Pass the tuple to the DBConnection class
    relationalDB = DBConnection_Alchemy(db_info)
    fetchData = FetchData(relationalDB.mydb)
    visualiseData = VisualiseData(relationalDB.mydb)

    # Fetch processed movie data
    business_and_movie_data = fetchData.fetch_and_process_movie_data()

    # Initialize ActorSearch and GenreSearch
    actor_search_app = ActorSearch(relationalDB.mydb)
    genre_search_app = GenreSearch(business_and_movie_data)

    # Initialize Tkinter root
    root = tk.Tk()

    # Instantiate AppGUI and pass `writeToLog` to DataAnalysis
    app_gui = AppGUI(
        master=root,
        actor_search_app=actor_search_app,
        genre_search_app=genre_search_app
    )

    # Pass AppGUI's `writeToLog` method to DataAnalysis
    data_analysis_app = DataAnalysis(connection=relationalDB.mydb, log_function=app_gui.writeToLog)

    # Assign DataAnalysis to AppGUI
    app_gui.data_analysis_app = data_analysis_app

    root.mainloop()

    # Close the connection
    relationalDB.disposeConnection()
    print("Connection closed")

if __name__ == "__main__":
    main()
