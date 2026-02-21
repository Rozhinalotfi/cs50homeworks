SELECT DISTINCT m1.title
FROM movies AS m1
JOIN stars AS s1 ON m1.id = s1.movie_id
JOIN people AS p1 ON s1.person_id = p1.id
WHERE p1.name = 'Helena Bonham Carter'
  AND m1.id IN (
    SELECT m2.id
    FROM movies AS m2
    JOIN stars AS s2 ON m2.id = s2.movie_id
    JOIN people AS p2 ON s2.person_id = p2.id
    WHERE p2.name = 'Johnny Depp'
  );
