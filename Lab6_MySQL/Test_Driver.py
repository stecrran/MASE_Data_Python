from DatabaseObj import DBConnection_Alchemy

def main():
    host = "db.relational-data.org"
    user = "guest"
    password = "relational"
    port = 3306
    database = "financial"

    # create tuple to store all this information
    db_info = (host, user, password, port, database)
    # pass the tuple to the DBConnecction class
    relationalDB = DBConnection_Alchemy(db_info)
    # ask the user to enter a table name
    table = input("\nEnter table name: ")
    # print the table name back to the user
    print("Table selected: {0}".format(table))
    # call the method selectTable and pass the table variable to it
    relationalDB.selectTable(table)
    # call a method that will visualise the client ratio
    relationalDB.visualiseClient()
    # close the connection
    relationalDB.disposeConnection()
    print("Connection closed")

if __name__ == "__main__":
    main()