from utils.dbutils import init_scoreboard

if __name__ == "__main__":
    print("Wrong file!")
    cont = input("Run main file? (Y/n)")
    if cont.upper() == "N":
        exit()
    else:
        from main import main_loop
        main_loop()

import sys
import hashlib
import sqlite3

from utils.dto import add_dto, UserDto, ScoreDto
import os

def hashword(p):
    m = hashlib.md5()
    m.update(p.encode('utf-8'))
    return m.hexdigest()

def hashword_new(p):
    m = hashlib.sha256()
    m.update(p.encode('utf-8'))
    return m.hexdigest()

def hashword_salts(p, s):
    if s is None:
        print("Please provide salt")
        sys.exit(-1)
    m = hashlib.pbkdf2_hmac('sha256', p.encode('utf-8'), s, 100_000)
    return m.hex()

def _quit(c):
    print("Quiting...")
    c.close()

def handle_register(name, pwd, con, cur):
    try:
        saltgen = os.urandom(16)
        cur.execute('''INSERT INTO users (name, password, salt) VALUES (?,?,?)''', (name, hashword_salts(pwd, saltgen), saltgen))
        add_dto(UserDto(id, name, saltgen, pwd))
    except sqlite3.IntegrityError:
        print("User already exists!")
    con.commit()

def get_user_id(cur, name):
    cur.execute('''SELECT id FROM users WHERE name = ?''', (name,))
    user_id = cur.fetchone()[0]
    return user_id

def handle_login(r, con, cur):
    name = r[1]
    pwd = r[2]
    loop2 = True
    while loop2:
        print("Quit: Q")
        i2 = input()
        if str(name.lower()).startswith("admin"):
            if i2.startswith("get"):
                if i2.split(" ")[1].lower() == "user":
                    print("User is " + name)
                elif i2.split(" ")[1].lower() == "pass":
                    print("Password is " + pwd)
                elif i2.split(" ")[1].lower() == "all":
                    cur.execute("SELECT * FROM users")
                    print(cur.fetchall())
                elif i2.split(" ")[1].lower() == "id":
                    print("ID is " + str(get_user_id(cur, name)))
            elif i2.startswith("del"):
                if i2.split(" ")[1].lower() == "table":
                    warn = input("WARNING! This action will delete THE WHOLE DB! DO NOT DO THIS! Are you sure you want to do this? (y/N)")
                    if warn.lower() == "y":
                        cur.execute('''DROP TABLE IF EXISTS users''')
                        con.commit()
                elif i2.split(" ")[1].lower() == "user":
                    try:
                        if i2.split(" ")[2].lower() == "all":
                            warn = input(
                                "WARNING! This action will delete the current user " + name + "! Are you sure you want to do this? (y/N)")
                            if warn.lower() == "y":
                                loop2 = False
                                cur.execute("DELETE FROM users")
                                con.commit()
                        else:
                            target = i2.split(" ")[2].lower()
                            print("Deleting " + target)
                            cur.execute("DELETE FROM users WHERE name = ?", (target,))
                            con.commit()
                    except:
                        print("Please provide user")
                elif i2.split(" ")[1].lower() == "scoreboard" or i2.split(" ")[1].lower() == "scores":
                    try:
                        if i2.split(" ")[2].lower() == "all":
                            print("Deleting scoreboard table")
                            cur.execute("DROP TABLE IF EXISTS scoreboard")
                    except IndexError:
                        print("Deleting scoreboard")
                        cur.execute("DELETE FROM scoreboard")
                    con.commit()

            elif i2.startswith("init"):
                if i2.split(" ")[1].lower() == "scoreboard":
                    print("Initializing Scoreboard")
                    init_scoreboard(con)


        elif i2.startswith("get "):
            if i2.split(" ")[1].lower() == "user":
                print("User is " + name)
            elif i2.split(" ")[1].lower() == "pass":
                print("Password is (hidden)")

        else:
            print("Invalid input")

        if i2.upper() == "Q":
            loop2 = False
            print("Quiting..")

        if i2.lower() == "commitall" or i2.lower() == "comitall":
            con.commit()
            print("Committed changes")

        try:
            if i2.startswith("get"):
                if i2.split(" ")[1].lower() == "scores":
                    cur.execute("SELECT * FROM scoreboard")
                    print(cur.fetchall())
            elif i2.startswith("add"):
                if i2.split(" ")[1].lower() == "score":
                    score = ScoreDto()
                    u1 = get_user_id(cur, name)
                    score.set_user1(int(u1))
                    loop3 = True
                    while loop3:
                        u2 = input("Who did you play against?")
                        try:
                            u2 = cur.execute("SELECT * FROM users WHERE name = ?", (u2,)).fetchone()[0]
                            loop3 = False
                        except TypeError:
                            print("User does not exist")


                    score.set_user2(int(u2))
                    score.set_score1(input("What was your score?"))
                    score.set_score2(input("What was your opponent's score?"))
                    cur.execute("INSERT INTO scoreboard (user1, user2, score1, score2) VALUES (?,?,?,?)", (score.get_user1(), score.get_user2(), score.get_score1(), score.get_score2()))
                    con.commit()
        except sqlite3.OperationalError:
            print("Something went wrong! Likely cause: scoreboard not initialized, run `init scoreboard`")