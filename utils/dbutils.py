def init_db(con):
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      name VARCHAR(255) NOT NULL UNIQUE,
      password CHAR(64) NOT NULL,
      salt BINARY(16) NOT NULL
    )
    """)

    init_scoreboard(con)
    con.commit()
    return cur


def init_scoreboard(con):
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS scoreboard (
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      user1_id BIGINT NOT NULL,
      user1_name VARCHAR(60) NOT NULL,
      user2_id BIGINT NOT NULL,
      user2_name VARCHAR(60) NOT NULL,
      score1 INT,
      score2 INT,
      CONSTRAINT fk_score_user1 FOREIGN KEY (user1_id) REFERENCES users(id),
      CONSTRAINT fk_score_user2 FOREIGN KEY (user2_id) REFERENCES users(id)
    )
    """)
    con.commit()