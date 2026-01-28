if __name__ == "__main__":
    print("Wrong file!")
    cont = input("Run main file? (Y/n)")
    if cont.upper() == "N":
        exit()
    else:
        from main import main_loop
        main_loop()

import sqlite3

def init_db():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    con.execute("PRAGMA foreign_keys = ON")
    cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER UNIQUE NOT NULL PRIMARY KEY, 
                    name text UNIQUE, password text, salt text)''')
    con.commit()
    return con, cur


def init_scoreboard(con):
    cur = con.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS scoreboard (
        user1 INTEGER NOT NULL REFERENCES users(id),
        user2 INTEGER NOT NULL REFERENCES users(id),
        score1 INTEGER,
        score2 INTEGER
    )''')
    con.commit()