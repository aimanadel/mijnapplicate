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

CREATE TABLE `vak`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `naam` VARCHAR(100) NOT NULL,
    PRIMARY KEY(`id`)
);

--  SCORE---
CREATE TABLE `score` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `leerling_id` INT NOT NULL,
    `vak_id` INT,
    `gemiddelde_score` DECIMAL(5,2),
    `vorige_score` DECIMAL(5,2),
    `trend` VARCHAR(50),
    `periode` DATE,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`leerling_id`) REFERENCES `leerling`(`id`)
);



--  VAARDIGHEID
CREATE TABLE `vaardigheid` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `leerling_id` INT NOT NULL,
    `naam` VARCHAR(100),
    `sterren` INT,
    `trend` VARCHAR(50),
    `bijgewerkt_op` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`leerling_id`) REFERENCES `leerling`(`id`)
) ENGINE=InnoDB;