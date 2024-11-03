from app.dal.utils import get_db_conn
from app.models.team_model import Team

def team_put(team: Team, team_id: int):
    with get_db_conn() as conn:
        c = conn.cursor()
        c.execute(
            """UPDATE teams SET code = ?, name = ? WHERE id = ?""",
            (team.code, team.name, team_id),
        )
        if c.rowcount == 0:
            return 1
        conn.commit()
        return 0