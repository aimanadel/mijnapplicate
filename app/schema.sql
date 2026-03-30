CREATE TABLE `docent`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(100) NOT NULL UNIQUE,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(`id`)
);

CREATE TABLE `Event`(
	`eventId` INT NOT NULL AUTO_INCREMENT,
    `description` VARCHAR(100) NOT NULL,
    `eventDate` DATETIME,
    `creationDate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ,        
    PRIMARY KEY(`eventId`)
);

<<<<<<< HEAD
CREATE TABLE `fout`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `leerling_id` INT NOT NULL,
    `categorie` VARCHAR(100) NOT NULL,
    `subcategorie` VARCHAR(100) NOT NULL,
    `aantal` INT NOT NULL,
    PRIMARY KEY(`id`)
);

CREATE TABLE `leerling`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `naam` VARCHAR(100) NOT NULL,
    `klas` VARCHAR(50) NOT NULL,
    PRIMARY KEY(`id`)
);

CREATE TABLE `resultaat`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `leerling_id` INT NOT NULL,
    `onderwerp` VARCHAR(100) NOT NULL,
    `score` INT NOT NULL,
    PRIMARY KEY(`id`),
    FOREIGN KEY (`leerling_id`) REFERENCES `leerling`(`id`)
);
=======

CREATE TABLE exercises (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    duration INTEGER,
    question_count INTEGER,
    color_code TEXT,
    status TEXT DEFAULT 'recommended',
);


>>>>>>> Tabel voor oefeningen sql gemaakt
