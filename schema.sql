CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE lists (
    id INTEGER PRIMARY KEY,
    title TEXT
);

CREATE TABLE users_lists (
    id INTEGER PRIMARY KEY,
    list_id INTEGER REFERENCES lists ON DELETE CASCADE,
    user_id INTEGER REFERENCES users
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    content TEXT
);

CREATE TABLE list_items (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items ON DELETE CASCADE,
    list_id INTEGER REFERENCES lists
);
