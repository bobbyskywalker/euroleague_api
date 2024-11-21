class Stats:
    def __init__(
        self,
        games_played,
        games_started,
        minutes_played,
        points_scored,
        two_pointers_made,
        two_pointers_attempted,
        three_pointers_made,
        three_pointers_attempted,
        free_throws_made,
        free_throws_attempted,
        offensive_rebounds,
        defensive_rebounds,
        assists,
        steals,
        turnovers,
        blocks,
        blocks_against,
        fouls,
        fouls_drawn,
        pir,
    ) -> None:
        self.games_played = games_played
        self.games_started = games_started
        self.minutes_played = minutes_played
        self.points_scored = points_scored
        self.two_pointers_made = two_pointers_made
        self.two_pointers_attempted = two_pointers_attempted
        self.three_pointers_made = three_pointers_made
        self.three_pointers_attempted = three_pointers_attempted
        self.free_throws_made = free_throws_made
        self.free_throws_attempted = free_throws_attempted
        self.offensive_rebounds = offensive_rebounds
        self.defensive_rebounds = defensive_rebounds
        self.assists = assists
        self.steals = steals
        self.turnovers = turnovers
        self.blocks = blocks
        self.blocks_against = blocks_against
        self.fouls = fouls
        self.fouls_drawn = fouls_drawn
        self.pir = pir


class Player:
    def __init__(self, code, name, age, team, stats, team_code) -> None:
        self.code = code
        self.name = name
        self.age = age
        self.team = team
        self.team_code = team_code
        self.stats = stats
