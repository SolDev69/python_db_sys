from flask import Flask, request, redirect
from flask import render_template
from utils import handle_login, handle_register, hashword_salts
from utils.dbutils import init_db
from utils.dto import find_salt_among_dtos
from mysql.connector import connect
from os import environ
from mysql.connector import errors

app = Flask(__name__)

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

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Handle registration logic here
        username = request.form["username"]
        password = request.form["password"]
        handle_register(username, password, con, cur)
        return redirect("/login")
    if request.method == "GET":
        return render_template("register.html")

saved_row = []
login_str = ""
@app.route("/login", methods=["GET", "POST"])
def login():
    global saved_row
    global login_str
    if request.method == "POST":
        # Handle login logic here
        username = request.form["username"]
        password = request.form["password"]
        salt = find_salt_among_dtos(username)
        # try:
        if salt is None:
            cur.execute("SELECT salt FROM users WHERE name = %s", (username,))
            salt = cur.fetchone()[0]
        cur.execute("SELECT * FROM users WHERE name = %s AND password = %s", (username, hashword_salts(password, salt)))
        row = cur.fetchone()
        if row:
            saved_row = row
            login_str = str(row[0]) + " : " + row[1]
            cur.execute("SELECT * FROM scoreboard")
            scores = cur.fetchall()
            return redirect("/scoreboard")
            #return redirect("/scoreboard.html", login = str(row[0]) + " : " + row[1])
        else:
            return "Invalid username or password"
        # except TypeError:
            # return "User does not exist with username and password provided"
    if request.method == "GET":
        return render_template("login.html")

@app.route("/scoreboard")
def scoreboard():
    global login_str
    cur.execute("SELECT * FROM scoreboard")
    scores = cur.fetchall()
    return render_template("scoreboard/index.html", login=login_str, scoreboard=scores)

@app.route("/scoreboard/addscore", methods=["POST", "GET"])
def add_score():
    global saved_row
    if request.method == "POST":
        u2 = 0
        user2_name = request.form["user2"]
        try:
            cur.execute("SELECT * FROM users WHERE name = %s", (user2_name,))
            u2 = cur.fetchone()[0]
        except TypeError:
            print("User does not exist")
        
        user2_id = int(u2)
        score1 = request.form["score1"]
        score2 = request.form["score2"]
        try:
            cur.execute('''INSERT INTO scoreboard (
                    user1_id, user1_name,
                    user2_id, user2_name,
                    score1, score2) VALUES (%s,%s,%s,%s,%s,%s)''', 
                    (saved_row[0], saved_row[1], user2_id, user2_name, score1, score2))
        except errors.IntegrityError:
            return "Error inserting score: invalid user input! Make sure you put in a real user"
        con.commit()
        cur.execute("SELECT * FROM scoreboard")
        scores = cur.fetchall()
        con.commit()
        login = login_str
        return redirect("/scoreboard")
    if request.method == "GET":
        return render_template("scoreboard/addscore.html")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug=True)