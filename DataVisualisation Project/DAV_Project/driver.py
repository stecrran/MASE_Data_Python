from FetchData import FetchData
from Database_Create import DBConnection_Alchemy

def main():
    host = "db.relational-data.org"
    user = "guest"
    password = "relational"
    port = 3306
    database = "imdb_full"

    # create tuple to store all this information
    db_info = (host, user, password, port, database)
    # pass the tuple to the DBConnecction class
    relationalDB = DBConnection_Alchemy(db_info)
    fetchData = FetchData(relationalDB.mydb)

    # call the method selectTable and pass the table variable to it
    #relationalDB.selectTable(table)

    # call a method that will visualise the client ratio
    #relationalDB.visualiseGenderDistribution()

    # close the connection
    fetchData.fetch_and_process_movie_data()
    relationalDB.disposeConnection()
    print("Connection closed")

if __name__ == "__main__":
    main()