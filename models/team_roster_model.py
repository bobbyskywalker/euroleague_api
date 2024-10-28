from pydantic import BaseModel


class TeamRoster(BaseModel):
    player_code: str
    player_first_name: str
    player_last_name: str
    player_yob: str
