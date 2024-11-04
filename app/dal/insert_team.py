from app.dal.utils import get_db_conn
from app.models.team_model import Team

# The object is responsible for inserting teams data into db
class TeamInserter:
    def __init__(self) -> None:
        pass

    def add_team(self, team: Team):
        with get_db_conn() as conn:
            c = conn.cursor()
            c.execute(
                """INSERT INTO teams (code, name) VALUES (?, ?)""", (team.code, team.name)
            )
            conn.commit()

    def add_team_picture(self, img_name: str, team_id: int):
        with get_db_conn() as conn:
            c = conn.cursor()
            c.execute(
                """UPDATE teams SET img_name = ? WHERE id = ?""",
                (img_name, team_id),
            )
            conn.commit()