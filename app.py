from flask import Flask, request, redirect
from flask import render_template
from utils import handle_login, handle_register, hashword_salts
from utils.dbutils import init_db
from utils.dto import find_salt_among_dtos
from mysql.connector import connect
from os import environ

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
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Handle login logic here
        username = request.form["username"]
        password = request.form["password"]
        salt = find_salt_among_dtos(username)
        try:
            if salt is None:
                cur.execute("SELECT salt FROM users WHERE name = %s", (username,))
                salt = cur.fetchone()[0]
            cur.execute("SELECT * FROM users WHERE name = %s AND password = %s", (username, hashword_salts(password, salt)))
            row = cur.fetchone()
            if row:
                return f"User {row[0]} : {row[1]} logged in!"
            else:
                return "Invalid username or password"
        except TypeError:
            return "User does not exist with username and password provided"
    if request.method == "GET":
        return render_template("login.html")