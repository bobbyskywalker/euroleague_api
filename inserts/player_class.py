from pydantic import BaseModel, Field
from datetime import datetime

# TODO: add constraints to both classes
class Player(BaseModel):
    code: str = Field(..., min_length=2, max_length=30)
    first_name: str = Field(..., min_length=2, max_length=30)
    last_name: str = Field(..., min_length=2, max_length=30)
    yob: int = Field(..., ge=1900, le=datetime.now().year)


class PlayerSeason(BaseModel):
    player_code: str = Field(..., min_length=2, max_length=30)
    team_code: str = Field(..., min_length=3, max_length=3)
    season_year: int = Field(..., ge=2000, le=datetime.now().year)

    # stats
    games_played: int = Field(..., ge=1, le=50) 
    points_scored: float = Field(..., ge=0, le=100)
    two_pointers_made: float = Field(..., ge=0, le=100)
    two_pointers_attempted: float = Field(..., ge=0, le=100)
    three_pointers_made: float = Field(..., ge=0, le=100)
    three_pointers_attempted: float = Field(..., ge=0, le=100)
    free_throws_made: float = Field(..., ge=0, le=100)
    free_throws_attempted: float = Field(..., ge=0, le=100)
    offensive_rebounds: float = Field(..., ge=0, le=100)
    defensive_rebounds: float = Field(..., ge=0, le=100)
    assists: float = Field(..., ge=0, le=100)
    steals: float = Field(..., ge=0, le=100)
    turnovers: float = Field(..., ge=0, le=100)
    blocks: float = Field(..., ge=0, le=100)
    fouls: float = Field(..., ge=0, le=100)
