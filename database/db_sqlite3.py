import sqlite3 as sq

def db_start():
    global base, cur

    base = sq.connect('dnd.db')
    cur = base.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Characters(id TEXT PRIMARY KEY, name TEXT, race TEXT, class TEXT, origin TEXT, level TEXT)")
    base.commit()

    cur.execute("INSERT INTO Characters VALUES (?, ?, ?, ?, ?, ?)", (id, '', '', '', '', ''))
    base.commit()

def db_insert(base, cur):
    cur.execute("INSERT INTO Characters VALUES (?, ?, ?, ?, ?, ?)", (id, '', '', '', '', ''))
    base.commit()