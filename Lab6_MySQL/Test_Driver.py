from DatabaseObj import DBConnection

def main():
    host = "db.relational-data.org"
    user = "guest"
    password = "relational"
    port = 3306
    database = "financial"

    db_info = (host, user, password, port, database)

    relationalDB = DBConnection(db_info)

    table = input("\nEnter table name: ")

    print("Table selected: {0}".format(table))

    relationalDB.selectTable(table)

    relationalDB.visualiseClient()

    relationalDB.disposeConnection()
    print("Connection closed")

if __name__ == "__main__":
    main()