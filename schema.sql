CREATE TABLE Reviews (
    id INTEGER PRIMARY KEY,
    comment TEXT
);

CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);