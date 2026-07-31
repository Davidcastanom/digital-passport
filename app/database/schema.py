from app.database.connection import validate_table_name

def get_key_info(table: str, conn):
    validate_table_name(table, conn)
    c = conn.cursor()
    pk_cols: set = set()
    for row in c.execute(f'PRAGMA table_info("{table}")'):
        if row[5] > 0:
            pk_cols.add(row[1])
    fk_cols: dict = {}
    for row in c.execute(f'PRAGMA foreign_key_list("{table}")'):
        fk_cols[row[3]] = row[2]
    return pk_cols, fk_cols
