DROP TABLE IF EXISTS user_word_reviews CASCADE;

DROP TABLE IF EXISTS definitions CASCADE;

DROP TABLE IF EXISTS words CASCADE;

DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE words (
    word_id SERIAL PRIMARY KEY,
    word VARCHAR(255) NOT NULL
);

CREATE INDEX idx_word ON words(word);

CREATE TABLE definitions (
    definition_id SERIAL PRIMARY KEY,
    definition TEXT NOT NULL,
    word_id INT NOT NULL REFERENCES words(word_id)
);

CREATE TABLE user_word_reviews (
    review_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id),
    word_id INT NOT NULL REFERENCES words(word_id),
    review_date DATE NOT NULL,
    ease_factor FLOAT NOT NULL DEFAULT 2.5,
    interval INT NOT NULL DEFAULT 1,
    repetitions INT NOT NULL DEFAULT 0,
    previous_interval INT DEFAULT NULL,
    review_quality INT NOT NULL DEFAULT 0
);

CREATE INDEX idx_user_word_review ON user_word_reviews(user_id, review_date);

CREATE INDEX idx_review_date ON user_word_reviews(review_date);
