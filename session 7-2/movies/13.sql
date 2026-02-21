SELECT DISTINCT people.name
FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
WHERE movies.id IN (
    SELECT m.id
    FROM movies AS m
    JOIN stars AS s ON m.id = s.movie_id
    JOIN people AS p ON s.person_id = p.id
    WHERE p.name = 'Kevin Bacon' AND p.birth = 1958
)
AND people.name != 'Kevin Bacon';