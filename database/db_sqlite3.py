import sqlite3 as sq


def db_start():
    global base, cur

    base = sq.connect('dnd.db')
    cur = base.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Characters(id INT PRIMARY KEY, name TEXT, race TEXT, class TEXT, origin TEXT, level INT)")
    base.commit()


async def db_insert(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO Characters VALUES (?, ?, ?, ?, ?, ?)", tuple(data.values()))
        base.commit()
