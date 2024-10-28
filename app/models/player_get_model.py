from pydantic import BaseModel


class PlayerGet(BaseModel):
    id: int
    first_name: str
    last_name: str
    team_name: str


class PlayerGetCarrer(BaseModel):
    id: int
    first_name: str
    last_name: str
    yob: str
    team_name: str
    year: int
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