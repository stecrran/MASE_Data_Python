import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="db.relational-data.org",
    port=3306,
    user="guest",
    password="relational",
    database="imdb_full"
)

# Create a cursor object
cursor = conn.cursor()

# Execute a query
cursor.execute(
"""select actors.name, movies2actors.as_character, movies.title from actors
inner join movies2actors on actors.actorid=movies2actors.actorid
inner join movies on movies.movieid=movies2actors.movieid
where movies.title like '%army of dark%'
and actors.name like '%bruce%'"""
)

# Fetch all the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the connection
conn.close()
