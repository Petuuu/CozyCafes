CREATE TABLE Reviews (
    id INTEGER PRIMARY KEY,
    user INTEGER REFERENCES Users(id),
    cafe TEXT,
    rating INTEGER,
    review_text TEXT,
    categories TEXT,
    date_created TEXT,
    date_edited TEXT
);

CREATE TABLE Comments (
    id INTEGER PRIMARY KEY,
    review INTEGER REFERENCES Reviews(id),
    user INTEGER REFERENCES Users(id),
    comment TEXT,
    date_created TEXT
);

CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    pfp BLOB
);