CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE lists (
    id INTEGER PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    list_id INTEGER REFERENCES lists
);

CREATE INDEX idx_item_list_ids ON items (list_id);