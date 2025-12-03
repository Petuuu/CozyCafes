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

CREATE INDEX idx_reviews_user ON Reviews (user);
CREATE INDEX idx_comments_review on Comments (review);
CREATE INDEX idx_comments_user on Comments (user);