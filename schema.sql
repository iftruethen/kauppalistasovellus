CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    class TEXT
);

INSERT INTO classes (class) VALUES ("ruokakauppa");
INSERT INTO classes (class) VALUES ("rautakauppa");
INSERT INTO classes (class) VALUES ("harrastusvälineliike");
INSERT INTO classes (class) VALUES ("eläintarvikeliike");
INSERT INTO classes (class) VALUES ("tavaratalo");
INSERT INTO classes (class) VALUES ("muu");

CREATE TABLE lists (
    id INTEGER PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES users,
    class_id INTEGER REFERENCES classes
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    list_id INTEGER REFERENCES lists ON DELETE CASCADE
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    user_id INTEGER REFERENCES users,
    list_id INTEGER REFERENCES lists ON DELETE CASCADE
);

CREATE TABLE shares (
    id INTEGER PRIMARY KEY,
    list_id INTEGER REFERENCES lists ON DELETE CASCADE,
    owner_user_id INTEGER REFERENCES users,
    approved_user_id INTEGER REFERENCES users,
    sharetype TEXT
);

CREATE INDEX idx_item_list_ids ON items (list_id);