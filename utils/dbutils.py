import sqlite3
import mysql.connector
import os
def init_db():
    con = mysql.connector.connect(
        host = os.environ["DB_HOST"],
        user = os.environ["DB_USER"],
        password = os.environ["DB_PASSWORD"],
        port = int(os.environ["DB_PORT"]),
        database = os.environ["DB_NAME"],
        autocommit = False # TODO: Change to true if needed
    )
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      name VARCHAR(255) NOT NULL UNIQUE,
      password CHAR(64) NOT NULL,
      salt BINARY(16) NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS scoreboard (
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      user1 BIGINT NOT NULL,
      user2 BIGINT NOT NULL,
      score1 INT,
      score2 INT,
      CONSTRAINT fk_score_user1 FOREIGN KEY (user1) REFERENCES users(id),
      CONSTRAINT fk_score_user2 FOREIGN KEY (user2) REFERENCES users(id)
    )
    """)
    con.commit()
    return con, cur


def init_scoreboard(con):
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS scoreboard (
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      user1 BIGINT NOT NULL,
      user2 BIGINT NOT NULL,
      score1 INT,
      score2 INT,
      CONSTRAINT fk_score_user1 FOREIGN KEY (user1) REFERENCES users(id),
      CONSTRAINT fk_score_user2 FOREIGN KEY (user2) REFERENCES users(id)
    )
    """)
    con.commit()