from db import query


def search_reviews():
    return query(
        """
        SELECT R.id, R.user, U.username, R.cafe, R.rating, R.review_text, R.date_created, R.date_edited
        FROM Reviews R
        JOIN Users U ON U.id = R.user
        ORDER BY R.date_created
        """
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


def search(q):
    return query(
        """
        SELECT R.id, R.user, U.username, R.cafe, R.rating, R.review_text, R.date_created, R.date_edited
        FROM Reviews R
        JOIN Users U ON U.id = R.user
        ORDER BY R.date_created
        """,
        ["%" + q + "%"],
    )
