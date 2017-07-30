DROP TABLE IF EXISTS `users_info`;
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
	`user_id`	INT(5) autoincrement,
	`username`	VARCHAR(50),
	`password`	VARCHAR(255),

	PRIMARY KEY `entries_pk` (`user_id`)
);

CREATE TABLE `users_info` (
	`user_id`	INT(5),
	`nickname`	VARCHAR(50),

	PRIMARY KEY `users_info_pk` (`user_id`),
	FOREIGN KEY `users_info-users_fk` (user_id) REFERENCES `users`(user_id)
);