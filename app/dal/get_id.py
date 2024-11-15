from app.dal.utils import get_db_conn

def get_id(first_name: str, last_name: str) -> int:
    # Ensure first_name and last_name are strings
    if isinstance(first_name, str) and isinstance(last_name, str):
        first_name = first_name.upper()
        last_name = last_name.upper()
    else:
        raise ValueError("Expected string values for first_name and last_name")
    
    with get_db_conn() as conn:
        c = conn.cursor()
        c.execute('''SELECT p.id
                     FROM players p
                    WHERE p.first_name = ? AND p.last_name = ?''', (first_name, last_name))
        fetched_id = c.fetchall()
        if not fetched_id:
            return None
        return fetched_id[0][0]