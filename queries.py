from db import query


def search_review_count():
    return query("SELECT COUNT(id) FROM Reviews")


def search_page_reviews(page, page_size):
    offset = page_size * (page - 1)
    return query(
        """
        SELECT R.id, R.user, U.username, R.cafe, R.rating, R.review_text,
            R.categories, R.date_created, R.date_edited, COUNT(C.id) AS count
        FROM Reviews R
        JOIN Users U ON U.id = R.user
        LEFT JOIN Comments C ON C.review = R.id
        GROUP BY R.id
        ORDER BY R.id DESC
        LIMIT ? OFFSET ?
        """,
        [page_size, offset],
    )


def search_user_reviews(user_id):
    return query(
        """
        SELECT R.id, R.user, U.username, R.cafe, R.rating, R.review_text,
            R.categories, R.date_created, R.date_edited, COUNT(C.id) AS count
        FROM Reviews R
        JOIN Users U ON U.id = R.user
        LEFT JOIN Comments C ON C.review = R.id
        WHERE R.user = ?
        GROUP BY R.id
        ORDER BY R.id DESC
        """,
        [user_id],
    )


def search(q):
    return query(
        """
        SELECT R.id, R.user, U.username, R.cafe, R.rating, R.review_text,
            R.categories, R.date_created, COUNT(C.id) AS count
        FROM Reviews R
        JOIN Users U ON U.id = R.user
        LEFT JOIN Comments C ON C.review = R.id
        WHERE R.date_created || ' ' || R.cafe || ' ' || R.rating || '/5 '
            || R.review_text || ' ' || R.date_created || U.username || R.categories LIKE ?
        GROUP BY R.id
        ORDER BY R.id DESC
        """,
        ["%" + q + "%"],
    )


def search_comments(comm_id):
    return query(
        """
        SELECT C.id, C.review, C.user, U.username, C.comment, C.date_created
        FROM Comments C
        JOIN Users U on U.id = C.user
        WHERE C.review = ?
        """,
        [comm_id],
    )


def fetch_review(review_id):
    return query(
        """
        SELECT R.id, R.user, U.username, R.cafe, R.rating, R.review_text,
            R.categories, R.date_created, R.date_edited
        FROM Reviews R
        JOIN Users U ON U.id = R.user
        WHERE R.id = ?""",
        [review_id],
    )


def fetch_user(user_id):
    return query(
        "SELECT id, username, pfp FROM Users WHERE id = ?",
        [user_id],
    )


def fetch_comment_section(review_id):
    return query("SELECT review, user FROM Comments WHERE id = ?", [review_id])
