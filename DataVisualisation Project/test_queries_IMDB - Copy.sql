use imdb_full;
SELECT count(*) FROM runningtimes order by time1 DESC;

SELECT 
    movies.movieid,
    movies.title,
    genres.genre,
    business.businesstext
FROM 
    movies
INNER JOIN 
    genres ON movies.movieid = genres.movieid
INNER JOIN 
    business ON movies.movieid = business.movieid
    where businesstext like "%USD%";

SELECT 
    movies.movieid,
    movies.title,
    GROUP_CONCAT(genres.genre SEPARATOR ', ') AS genres,
    business.businesstext
FROM 
    movies
INNER JOIN 
    genres ON movies.movieid = genres.movieid
INNER JOIN 
    business ON movies.movieid = business.movieid
WHERE 
    business.businesstext LIKE "%USD%"
GROUP BY 
    movies.movieid, movies.title, business.businesstext;






