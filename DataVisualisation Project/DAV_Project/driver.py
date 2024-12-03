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

    # Fetch the processed data
    grouped = fetchData.fetch_and_process_movie_data()

    # Initialize apps
    actor_search_app = ActorSearch(relationalDB.mydb)
    genre_search_app = GenreSearch(grouped)

    # Create the main Tk instance
    root = tk.Tk()
    AppGUI(master=root, actor_search_app=actor_search_app, genre_search_app=genre_search_app)

    root.mainloop()

    #VisualiseData.plot_genre_revenue_by_year(grouped)

    # Close the connection
    relationalDB.disposeConnection()
    print("Connection closed")


if __name__ == "__main__":
    main()
