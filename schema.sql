CREATE TABLE Reviews (
    id INTEGER PRIMARY KEY,
    user INTEGER,
    cafe TEXT,
    rating INTEGER,
    review_text TEXT,
    date_created TEXT,
    date_edited TEXT,
    FOREIGN KEY(user) REFERENCES Users(id)
);

CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    pfp BLOB
);