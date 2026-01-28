import hashlib
import sqlite3

from dto import add_dto, UserDto


def hashword(p):
    m = hashlib.md5()
    m.update(p.encode('utf-8'))
    return m.hexdigest()

def hashword_new(p):
    m = hashlib.sha256()
    m.update(p.encode('utf-8'))
    return m.hexdigest()

def _quit(c):
    print("Quiting...")
    c.close()

def handle_register(name, pwd, con, cur):
    try:
        cur.execute('''INSERT INTO users (name, password) VALUES (?,?)''', (name, hashword_new(pwd)))
    except sqlite3.IntegrityError:
        print("User already exists!")

    con.commit()

def handle_login(r, con, cur):
    id = r[0]
    name = r[1]
    pwd = r[2]
    add_dto(UserDto(id, name, pwd))
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
            elif i2.startswith("del"):
                if i2.split(" ")[1].lower() == "all":
                    warn = input("WARNING! This action will delete the current user " + name + "! Are you sure you want to do this? (y/N)")
                    if warn.lower() == "y":
                        loop2 = False
                        cur.execute("DELETE FROM users")
                        con.commit()
                elif i2.split(" ")[1].lower() == "table":
                    warn = input("WARNING! This action will delete THE WHOLE DB! DO NOT DO THIS! Are you sure you want to do this? (y/N)")
                    if warn.lower() == "y":
                        cur.execute('''DROP TABLE IF EXISTS users''')
                        con.commit()

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

