from app.dal.utils import get_db_conn

def rm_player(player_code: str):
    with get_db_conn() as conn:
        c = conn.cursor()
        c.execute("""DELETE FROM players WHERE code = ?""", (player_code,))
        if c.rowcount == 0:
            return 1
        conn.commit()
        return 0