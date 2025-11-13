CREATE TABLE Reviews (
    id INTEGER PRIMARY KEY,
    user INTEGER,
    cafe TEXT,
    rating INTEGER,
    review_text TEXT,
    FOREIGN KEY(user) REFERENCES Users(id)
);

CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);