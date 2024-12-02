from FetchData import FetchData
from ActorSearch import ActorSearch
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
    fetchData.fetch_and_process_movie_data()

    # Run the Actor Movie Search App
    #actor_search_app = ActorSearch(relationalDB.mydb)
    #actor_search_app.run()

    # Close the connection
    relationalDB.disposeConnection()
    print("Connection closed")


if __name__ == "__main__":
    main()
