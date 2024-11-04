from app.dal.utils import get_db_conn

def rm_team(team_id: str) -> int:
    with get_db_conn() as conn:
        c = conn.cursor()
        c.execute("""DELETE FROM teams WHERE id = ?""", (team_id,))
        if c.rowcount == 0:
            return 1
        conn.commit()
        return 0