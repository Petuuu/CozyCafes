from random import randint
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM Users")
db.execute("DELETE FROM Reviews")
db.execute("DELETE FROM Comments")

user_count = 1000
review_count = 10**5
comment_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO Users (username) VALUES (?)", ["user" + str(i)])

for i in range(1, review_count + 1):
    s = str(i)
    db.execute(
        """
        INSERT INTO Reviews (user, cafe, rating, review_text, date_created)
        VALUES (?, ?, ?, ?, datetime('now'))
        """,
        [i % 1000, "cafe" + s, randint(1, 5), "message" + s],
    )

for i in range(1, comment_count + 1):
    db.execute(
        """
        INSERT INTO Comments (review, user, comment, date_created)
        VALUES (?, ?, ?, datetime('now'))
        """,
        [i % 10**5, i % 1000, "comment" + str(i)],
    )

db.commit()
db.close()
