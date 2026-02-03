from utils import handle_login, handle_register, hashword_salts
from utils.dbutils import init_db
from utils.dto import find_salt_among_dtos
from mysql.connector import connect
from os import environ
def main_loop():
    try:
        con = connect(
            host = environ["DB_HOST"],
            user = environ["DB_USER"],
            password = environ["DB_PASSWORD"],
            port = int(environ["DB_PORT"]),
            database = environ["DB_NAME"],
            autocommit = False # TODO: Change to true if needed
        )
    except KeyError: 
        raise EnvironmentError("Please set DB environment variables (DB_HOST, DB_USER, DB_PASSWORD, DB_PORT, DB_NAME) and rerun!")

    cur = init_db(con)
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
                    cur.execute("SELECT salt FROM users WHERE name = %s", (username,))
                    salt = cur.fetchone()[0]
                cur.execute("SELECT * FROM users WHERE name = %s AND password = %s", (username, hashword_salts(password, salt)))
                row = cur.fetchone()
                print("User " + str(row[0]) + " : " + row[1] + " logged in!")
                handle_login(row, con, cur)
            except TypeError:
                print("User does not exist with username and password provided")

        elif i == "R":
            username = input("Username: ")
            password = input("Password: ")
            handle_register(username, password, con, cur)
        elif i == "Q":
            con.commit()
            con.close()
            loop = False
        else:
            print("Invalid input")
    return loop

if __name__ == "__main__":
    main_loop()