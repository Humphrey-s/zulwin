-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS zulwin_dev_db;
CREATE USER IF NOT EXISTS 'zulwin_dev'@'localhost' IDENTIFIED BY '48maran88';
GRANT ALL PRIVILEGES ON `zulwin_dev_db`.* TO 'zulwin_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'zulwin_dev'@'localhost';
FLUSH PRIVILEGES;

USE zulwin_dev_db;

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (`id` varchar(60) NOT NULL, `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP, `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP, `username` varchar(128) NOT NULL, `carts` varchar(128), PRIMARY KEY (`id`)
);


CREATE TABLE `items` (
	`id` varchar(60) NOT NULL,                                                                                              `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,                                                               `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`name` varchar(128) NOT NULL,
	`category` varchar(128) NOT NULL,
	`seller_id` varchar(60) NOT NULL,
	KEY `seller_id` (`seller_id`),
	CONSTRAINT `items_ibfk_1` FOREIGN KEY (`seller_id`) REFERENCES `users` (`id`)
);
