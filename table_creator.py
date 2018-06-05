import sqlite3

if input("Please confirm that you want to reset the database by typing \"yes\": ") != "yes":
    print("No yes detected, quitting program!")
    exit()
print("Resetting database")


db = sqlite3.connect("data/toots.db")

db.execute("DROP TABLE IF EXISTS raw_toots")
db.execute("DROP TABLE IF EXISTS terms")

db.execute(
    """
CREATE TABLE raw_toots (
  id INT,
  created_at DATETIME,
  added_at DATETIME,
  content TEXT,
  language VARCHAR(5),
  reblogs_count INT,
  instance TEXT,
  PRIMARY KEY (id, instance)

)"""
)

db.execute(
    """
CREATE TABLE terms (
  created_at DATETIME,
  term TEXT

)"""
)

