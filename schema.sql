CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT,
	password TEXT
);

CREATE TABLE discussions (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	topic TEXT, 
	created TIMESTAMP,
	likes INTEGER
);


