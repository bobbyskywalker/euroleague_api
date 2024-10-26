from pydantic import BaseModel, Field, condecimal
from datetime import datetime


class Player(BaseModel):
    first_name: str
    last_name: str
    yob: int = Field(..., ge=1900, le = 2025)

    # trigger an error if team not exists in particular season or doesnt exist at all
    team_code: str
    season_year: int = Field(..., ge=2000, le=datetime.now().year)

    #stats
    points_scored: float = condecimal(max_digits=2, decimal_places=1)
    two_pointers_made: float = condecimal(max_digits=2, decimal_places=1)
    two_pointers_attempted: float = condecimal(max_digits=2, decimal_places=1)
    three_pointers_made: float = condecimal(max_digits=2, decimal_places=1)
    three_pointers_attempted: float = condecimal(max_digits=2, decimal_places=1)
    free_throws_made: float = condecimal(max_digits=2, decimal_places=1)
    free_throws_attempted: float = condecimal(max_digits=2, decimal_places=1)
    offensive_rebounds: float = condecimal(max_digits=2, decimal_places=1)
    defensive_rebounds: float = condecimal(max_digits=2, decimal_places=1)
    assists: float = condecimal(max_digits=2, decimal_places=1)
    steals: float = condecimal(max_digits=2, decimal_places=1)
    turnovers: float = condecimal(max_digits=2, decimal_places=1)
    blocks: float = condecimal(max_digits=2, decimal_places=1)
    fouls: float = condecimal(max_digits=2, decimal_places=1)
