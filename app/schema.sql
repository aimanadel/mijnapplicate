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

CREATE TABLE result (
    -- Unique ID number for each saved result.
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- The ID of the exercise that this result is for, linking to the exercises table.
    exercise_id INTEGER,
    -- The grade achieved in the exercise, stored as a real number.
    score REAL,
    -- The date and time when the exercise was completed, defaulting to the current timestamp.
    completion_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    /** Establishing a foreign key relationship to ensure that each result is associated with a valid exercise.
     * You can't save a result for a lesson that doesn't exist in the exercises table.
     */
    FOREIGN KEY (exercise_id) REFERENCES exercises(id)
);