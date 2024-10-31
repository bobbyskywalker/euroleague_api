from app.dal.utils import get_db_conn
from app.models.search_player_class import SearchPlayer

def find_player(attributes: SearchPlayer, page, limit):
    offset = (page - 1) * limit
    query = 'SELECT * FROM players WHERE 1=1'
    params = []
    if attributes.first_name:
        query += ' AND first_name = ?'
        params.append(attributes.first_name)
    if attributes.last_name:
        query += ' AND last_name = ?'
        params.append(attributes.last_name)
    if attributes.yob_from:
        yob_from_str = f"{attributes.yob_from}-01-01"
        query += ' AND yob >= ?'
        params.append(yob_from_str)
    if attributes.yob_to:
        yob_to_str = f"{attributes.yob_to}-01-01"
        query += ' AND yob <= ?'
        params.append(yob_to_str)

    # pagination
    query += ' LIMIT ? OFFSET ?'
    params.append(limit)
    params.append(offset)

    with get_db_conn() as conn:
        c = conn.cursor()
        c.execute(f'''{query}''', tuple(params))
        players = c.fetchall()
        conn.commit()
    return players
        
