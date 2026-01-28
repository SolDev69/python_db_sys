from utils import *

conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER UNIQUE NOT NULL PRIMARY KEY, name text UNIQUE, password text)''')
loop = True

while loop:
    print("Login: L")
    print("Register: R")
    print("Quit: Q")
    i = input().upper()
    if i == "L":
        username = input("Username: ")
        password = input("Password: ")
        cur.execute("SELECT * FROM users WHERE name = ? AND password = ?", (username, hashword_new(password)))
        row = cur.fetchone()
        if row is None:
            print("User does not exist")
        else:
            if row[1] != username:
                print("Incorrect username")
            elif row[2] != hashword_new(password):
                print("Incorrect password")
            else:
                print("User " + str(row[0]) + " : " + row[1] + " logged in!")
                handle_login(row, conn, cur)

    elif i == "R":
        username = input("Username: ")
        password = input("Password: ")
        handle_register(username, password, conn, cur)
    elif i == "Q":
        conn.commit()
        conn.close()
        loop = False
    else:
        print("Invalid input")