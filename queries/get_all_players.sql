SELECT DISTINCT p.id, p.first_name, p.last_name, t.name
FROM players p 
JOIN playersTeams pt ON p.id = pt.player_id 
JOIN teams t ON pt.team_id  = t.id 
JOIN seasons s ON pt.season_id = s.id
WHERE s."year" = 2024   