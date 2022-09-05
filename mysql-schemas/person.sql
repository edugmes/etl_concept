-- datatestdb.person definition
DROP TABLE IF exists person;

CREATE TABLE `person` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(10) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `interest1` varchar(100) DEFAULT NULL,
  `interest2` varchar(100) DEFAULT NULL,
  `interest3` varchar(100) DEFAULT NULL,
  `interest4` varchar(100) DEFAULT NULL,
  `phone_number` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;