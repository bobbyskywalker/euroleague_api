from app.dal.utils import get_db_conn

def get_id(first_name: str, last_name: str) -> int:
    with get_db_conn() as conn:
        c = conn.cursor()
        c.execute('''SELECT p.id
                   FROM players p
                  WHERE p.first_name = ? AND p.last_name = ?''', (first_name, last_name))
        fetched_id = c.fetchall()
        if not fetched_id:
            return None
        return fetched_id[0][0]
