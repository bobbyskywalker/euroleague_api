SELECT DISTINCT t.id, t.code, t.name 
FROM teams t
JOIN playersTeams pt on t.id = pt.team_id 
JOIN seasons s on s.id  = pt.season_id 
WHERE s."year" = ?