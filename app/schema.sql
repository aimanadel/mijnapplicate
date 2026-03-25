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