import sqlite3

def init_db():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER UNIQUE NOT NULL PRIMARY KEY, 
                    name text UNIQUE, password text, salt text)''')
    con.commit()
    return con, cur