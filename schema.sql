DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS discussions CASCADE;
DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS tags CASCADE;

CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT,
	password TEXT,
	role INTEGER
);

CREATE TABLE discussions (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	topic TEXT, 
	created TIMESTAMP,
	likes INTEGER,
	content TEXT,
	visible INTEGER
);

CREATE TABLE comments (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	discussion_id INTEGER REFERENCES discussions,
	comment TEXT,
	created TIMESTAMP,
	likes INTEGER
);

CREATE TABLE tags (
	id SERIAL PRIMARY KEY,
	discussion_id INTEGER REFERENCES discussions,
	tag TEXT,
	created TIMESTAMP
);
