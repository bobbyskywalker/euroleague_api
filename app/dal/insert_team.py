from app.dal.utils import get_db_conn
from app.models.team_model import Team

def add_team(team: Team):
    with get_db_conn() as conn:
        c = conn.cursor()
        c.execute(
            """INSERT INTO teams (code, name) VALUES (?, ?)""", (team.code, team.name)
        )
        conn.commit()
