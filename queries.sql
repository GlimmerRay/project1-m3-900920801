CREATE TABLE users (
    username varchar(32) UNIQUE,
    artist_ids varchar(64)[]
);

-- Insert a new user
INSERT INTO users(username)
VALUES ('brandon');

-- Append a artist id to a user's list
UPDATE users
SET artist_ids = artist_ids || '{"12345"}'
WHERE username = 'brandon';

-- Drop a table
DROP TABLE users;