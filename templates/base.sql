CREATE DATABASE shopping;
USE shopping;

CREATE TABLE IF NOT EXISTS User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(255) DEFAULT "Pas de description",
    price INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Payment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_date DATE DEFAULT now(),
    comment VARCHAR(255) DEFAULT "no comment",
    FOREIGN KEY (user_id) REFERENCES User(id)
);