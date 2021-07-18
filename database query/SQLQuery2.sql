USE mybooks

CREATE TABLE book(
	id int PRIMARY KEY IDENTITY(1,1),
	title VARCHAR(255),
	author VARCHAR(255),
	ISBN int
);