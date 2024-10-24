SELECT 
    movies.movieid,
    movies.title,
    GROUP_CONCAT(genres.genre SEPARATOR ', ') AS genres,
    CONCAT('USD ', REGEXP_SUBSTR(SUBSTRING(business.businesstext, LOCATE('USD', business.businesstext) + 4), '^[0-9,]+')) AS business_info
FROM 
    movies
INNER JOIN 
    genres ON movies.movieid = genres.movieid
INNER JOIN 
    business ON movies.movieid = business.movieid
WHERE 
    business.businesstext LIKE '%USD%'
GROUP BY 
    movies.movieid, movies.title, business_info;


