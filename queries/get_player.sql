SELECT DISTINCT p.id, p.first_name, p.last_name, p.yob, t.name, s.year, st.points_scored, st.two_pointers_made, st.two_pointers_attempted, st.three_pointers_made , st.three_pointers_attempted, st.free_throws_made , st.free_throws_attempted, st.offensive_rebounds, st.defensive_rebounds, st.assists, st.steals, st.turnovers , st.blocks, st.fouls 
FROM players p 
JOIN playersTeams pt ON p.id = pt.player_id
JOIN stats st ON pt.id = st.player_team_id 
JOIN teams t ON pt.team_id  = t.id 
JOIN seasons s ON pt.season_id = s.id
WHERE p.first_name = ? AND p.last_name = ?