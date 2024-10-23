SELECT p.code, p.first_name, p.last_name, p.yob
FROM players p 
JOIN playersTeams pt on p.id = pt.player_id 
JOIN teams t on t.id = pt.team_id
JOIN seasons s on s.id = pt.season_id 
WHERE s."year" = 2017 and t.code = 'MAD'