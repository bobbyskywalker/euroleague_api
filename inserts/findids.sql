--FIND PLAYER ID
SELECT DISTINCT p.id, p.first_name, p.last_name 
FROM players p
WHERE p.first_name = ? AND p.last_name = ?

--FIND TEAM ID
SELECT DISTINCT t.id 
FROM teams t 
WHERE t.code = ?

--FIND SEASON ID
SELECT DISTINCT s.id
FROM seasons s 
WHERE s."year" = ?