from pydantic import BaseModel, Field

# TODO: add constraints to both classes
class Player(BaseModel):
    code: str
    first_name: str
    last_name: str
    yob: int = Field(..., ge=1900, le=2025)


class PlayerSeason(BaseModel):
    player_code: str
    team_code: str
    season_year: int = Field(..., ge=2000, le=2025)

    # stats
    games_played: int
    points_scored: float
    two_pointers_made: float
    two_pointers_attempted: float
    three_pointers_made: float
    three_pointers_attempted: float
    free_throws_made: float
    free_throws_attempted: float
    offensive_rebounds: float
    defensive_rebounds: float
    assists: float
    steals: float
    turnovers: float
    blocks: float
    fouls: float
