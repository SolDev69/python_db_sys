from utils import handle_login, handle_register, hashword_salts
from utils.dbutils import init_db
from utils.dto import find_salt_among_dtos

conn, cur = init_db()

def main_loop():
    loop = True
    while loop:
        print("Login: L")
        print("Register: R")
        print("Quit: Q")
        i = input().upper()
        if i == "L":
            username = input("Username: ")
            password = input("Password: ")
            salt = find_salt_among_dtos(username)
            try:
                if salt is None:
                    cur.execute("SELECT salt FROM users WHERE name = ?", (username,))
                    salt = cur.fetchone()[0]
                cur.execute("SELECT * FROM users WHERE name = ? AND password = ?", (username, hashword_salts(password, salt)))
                row = cur.fetchone()
                print("User " + str(row[0]) + " : " + row[1] + " logged in!")
                handle_login(row, conn, cur)
            except TypeError:
                print("User does not exist with username and password provided")

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
    return loop

if __name__ == "__main__":
    main_loop()