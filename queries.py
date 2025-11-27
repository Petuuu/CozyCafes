from db import query


def search_reviews():
    return query(
        """
        SELECT R.id, R.user, U.username, R.cafe, R.rating, R.review_text, R.date_created, R.date_edited
        FROM Reviews R
        JOIN Users U ON U.id = R.user
        ORDER BY R.date_created DESC
        """
    )


def search_user_reviews(id):
    return query(
        """
        SELECT R.id, R.user, U.username, R.cafe, R.rating, R.review_text, R.date_created, R.date_edited
        FROM Reviews R
        JOIN Users U ON U.id = R.user
        WHERE R.user = ?
        ORDER BY R.date_created DESC
        """,
        [id],
    )


def search(q):
    return query(
        """
        SELECT R.id, R.user, U.username, R.cafe, R.rating, R.review_text, R.date_created, R.date_edited
        FROM Reviews R
        JOIN Users U ON U.id = R.user
        WHERE R.date_created || ' ' || R.cafe || ' ' || R.rating || '/5 ' || R.review_text || ' ' || R.date_created LIKE ?
        ORDER BY R.date_created
        """,
        ["%" + q + "%"],
    )


def search_comments(id):
    return query(
        """
        SELECT C.id, C.review, C.user, U.username, C.comment, C.date_created
        FROM Comments C
        JOIN Users U on U.id = C.user
        WHERE C.review = ?
        """,
        [id],
    )


def fetch_review(id):
    return query(
        """
        SELECT R.id, R.user, U.username, R.cafe, R.rating, R.review_text, R.date_created, R.date_edited
        FROM Reviews R
        JOIN Users U ON U.id = R.user
        WHERE R.id = ?""",
        [id],
    )


def fetch_user(id):
    return query(
        """
        SELECT id, username, pfp
        FROM Users
        WHERE id = ?""",
        [id],
    )
