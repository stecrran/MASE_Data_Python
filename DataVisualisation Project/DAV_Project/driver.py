from FetchData import FetchData
from ActorSearch import ActorSearch
from GenreSearch import GenreSearch
from VisualiseData import VisualiseData
from DataAnalysis import DataAnalysis
from DatabaseAccess import DBConnection_Alchemy

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
    analyseData = DataAnalysis(relationalDB.mydb)

    # fetchData
    #fetchData.fetch_and_process_movie_data()
    # fetchData.count_genre_by_year('comedy')

    business_and_movie_data = fetchData.fetch_and_process_movie_data()

    # visualise data
    """
    business_and_movie_data = fetchData.fetch_and_process_movie_data()
    visualiseData.plot_percentage_profit_loss_by_year(business_and_movie_data)
    visualiseData.plot_percentage_profit_loss_by_year_zoomed(business_and_movie_data)
    visualiseData.plot_percentage_profit_loss_by_year_100(business_and_movie_data)
    """
    #visualiseData.plot_all_genres_by_year(business_and_movie_data)

    # Run the Actor Movie Search App
    #actor_search_app = ActorSearch(relationalDB.mydb)
    #actor_search_app.run()

    # Run GenreSearch App
    grouped = fetchData.fetch_and_process_movie_data()
    genre_search_app = GenreSearch(grouped)
    genre_search_app.run()

    # Close the connection
    relationalDB.disposeConnection()
    print("Connection closed")


if __name__ == "__main__":
    main()
