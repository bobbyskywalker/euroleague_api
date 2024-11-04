from app.dal.utils import get_db_conn
from app.models.player_insert_model import Player

def player_put(player: Player, player_id: str) -> int:
    with get_db_conn() as conn:
        c = conn.cursor()
        c.execute(
            """UPDATE players SET code = ?, first_name = ?, last_name = ?, yob = ? WHERE id = ?""",
            (player.code, player.first_name.upper(), player.last_name.upper(), f"{player.yob}-01-01", player_id),
        )
        if c.rowcount == 0:
            return 1
        conn.commit()
        return 0