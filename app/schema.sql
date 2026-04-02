CREATE TABLE Event (
    eventId INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    eventDate DATETIME,
    creationDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);


/** Exercise table to store exercise details such as title, description, duration, question count, color code, and status.
 * The status field can be used to indicate whether an exercise is recommended or not.
 */

CREATE TABLE exercises (
    -- Unique ID number for each exercise, counts up automatically: 1,2,3 etc.
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- The name of the exercise.
    title TEXT NOT NULL,
    -- A short explanation of what the exercise is about.
    description TEXT,
    -- How long the exercise takes.
    duration INTEGER,
    -- How many questions the exercise has.
    question_count INTEGER,
    -- A color to visually represent the exercise.
    color_code TEXT,
    -- Whether the exercise is recommended or not, default is 'recommended'.
    status TEXT DEFAULT 'recommended'
);

/** Result table to store the results of exercises, including the score and completion time.
 * It has a foreign key relationship with the exercises table to link each result to a specific exercise.
 */

CREATE TABLE `leerling`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `naam` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `wachtwoord_hash` VARCHAR(255) NOT NULL,
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



