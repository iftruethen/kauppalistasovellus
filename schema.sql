CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
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

CREATE TABLE classifications (
    id INTEGER PRIMARY KEY,
    list_id INTEGER REFERENCES lists,
    user_id INTEGER REFERENCES users,
    classification TEXT NOT NULL
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    user_id INTEGER REFERENCES users,
    list_id INTEGER REFERENCES lists
);

CREATE TABLE shares (
    id INTEGER PRIMARY KEY,
    list_id INTEGER REFERENCES lists,
    owner_user_id INTEGER REFERENCES users,
    approved_user_id INTEGER REFERENCES users,
    sharetype TEXT
);

CREATE INDEX idx_item_list_ids ON items (list_id);