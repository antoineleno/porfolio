-- prepares a MySQL server for the project

SET GLOBAL validate_password.policy = LOW;
DROP DATABASE IF EXISTS campus_dev_db;
CREATE DATABASE IF NOT EXISTS campus_dev_db;
CREATE USER IF NOT EXISTS 'campus_dev'@'localhost' IDENTIFIED BY 'campus_dev_pwd';
GRANT ALL PRIVILEGES ON `campus_dev_db`.* TO 'campus_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'campus_dev'@'localhost';
FLUSH PRIVILEGES;
