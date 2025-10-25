SCHEMA_SQL = """
-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name TEXT
);

-- Cards table
CREATE TABLE cards (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    tags TEXT[] NOT NULL,
    price TEXT,
    address TEXT
);

-- Liked cards table
CREATE TABLE liked_cards (
    user_id INT REFERENCES users(user_id),
    card_id INT REFERENCES cards(id),
    PRIMARY KEY (user_id, card_id)
);
"""