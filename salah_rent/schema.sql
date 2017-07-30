DROP TABLE IF EXISTS `users_info`;
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
	`user_id`	INTEGER PRIMARY KEY autoincrement,
	`username`	VARCHAR,
	`password`	VARCHAR
);

CREATE TABLE `users_info` (
	`user_id`	INT PRIMARY KEY,
	`nickname`	VARCHAR,

	FOREIGN KEY(user_id) REFERENCES `users`(user_id)
);

INSERT INTO `users` (username, password)
VALUES ('admin', '1234');