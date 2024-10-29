from app.dal.utils import get_db_conn
from app.models.team_model import Team


def team_put(team: Team, old_code):
    with get_db_conn() as conn:
        c = conn.cursor()
        c.execute(
            """UPDATE teams SET code = ?, name = ? WHERE code = ?""",
            (team.code, team.name, old_code),
        )
        if c.rowcount == 0:
            return 1
        conn.commit()
        return 0