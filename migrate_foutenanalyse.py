# Migration script voor nieuwe foutenanalyse tabellen

from app.db import execute_query

def migrate_foutenanalyse():
    """Voeg nieuwe tabellen toe voor foutenanalyse."""

    # Subject tabel
    subject_table = """
    CREATE TABLE IF NOT EXISTS `subject` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(100) NOT NULL,
        PRIMARY KEY (`id`)
    );
    """

    # Question tabel
    question_table = """
    CREATE TABLE IF NOT EXISTS `question` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `subject_id` INT NOT NULL,
        `question_text` TEXT NOT NULL,
        `solution_text` TEXT,
        `difficulty` VARCHAR(50),
        `max_score` INT NOT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`subject_id`) REFERENCES `subject`(`id`)
    );
    """

    # StudentAnswer tabel
    student_answer_table = """
    CREATE TABLE IF NOT EXISTS `student_answer` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `student_id` INT NOT NULL,
        `question_id` INT NOT NULL,
        `student_answer` TEXT,
        `score` INT NOT NULL,
        `max_score` INT NOT NULL,
        `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`student_id`) REFERENCES `leerling`(`id`),
        FOREIGN KEY (`question_id`) REFERENCES `question`(`id`)
    );
    """

    # MistakeAnalysis tabel
    mistake_analysis_table = """
    CREATE TABLE IF NOT EXISTS `mistake_analysis` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `student_answer_id` INT NOT NULL,
        `mistake_type` VARCHAR(100) NOT NULL,
        `feedback_text` TEXT,
        `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`student_answer_id`) REFERENCES `student_answer`(`id`)
    );
    """

    tables = [subject_table, question_table, student_answer_table, mistake_analysis_table]

    for table_sql in tables:
        print(f"Creating table...")
        result = execute_query(table_sql)
        print(f"Result: {result}")

def seed_foutenanalyse():
    """Voeg seed data toe voor foutenanalyse."""

    # Seed subjects
    subjects = [
        "INSERT INTO subject (name) VALUES ('Wiskunde A');",
        "INSERT INTO subject (name) VALUES ('Wiskunde B');",
        "INSERT INTO subject (name) VALUES ('Wiskunde C');",
        "INSERT INTO subject (name) VALUES ('Natuurkunde');"
    ]

    # Seed questions
    questions = [
        "INSERT INTO question (subject_id, question_text, solution_text, difficulty, max_score) VALUES (1, 'Bereken 2 + 2', 'Het antwoord is 4', 'makkelijk', 10);",
        "INSERT INTO question (subject_id, question_text, solution_text, difficulty, max_score) VALUES (1, 'Bereken de afgeleide van x^2', 'De afgeleide is 2x', 'gemiddeld', 15);",
        "INSERT INTO question (subject_id, question_text, solution_text, difficulty, max_score) VALUES (2, 'Los de vergelijking x + 3 = 7 op', 'x = 4', 'makkelijk', 10);",
        "INSERT INTO question (subject_id, question_text, solution_text, difficulty, max_score) VALUES (3, 'Bereken de integraal van 2x dx', 'Het antwoord is x^2 + C', 'moeilijk', 20);",
        "INSERT INTO question (subject_id, question_text, solution_text, difficulty, max_score) VALUES (4, 'Wat is de snelheid van licht?', '299792458 m/s', 'gemiddeld', 10);"
    ]

    # Seed student answers
    answers = [
        "INSERT INTO student_answer (student_id, question_id, student_answer, score, max_score) VALUES (1, 1, '4', 10, 10);",
        "INSERT INTO student_answer (student_id, question_id, student_answer, score, max_score) VALUES (1, 2, 'x', 5, 15);",
        "INSERT INTO student_answer (student_id, question_id, student_answer, score, max_score) VALUES (1, 3, '4', 10, 10);",
        "INSERT INTO student_answer (student_id, question_id, student_answer, score, max_score) VALUES (1, 4, 'x^2', 10, 20);",
        "INSERT INTO student_answer (student_id, question_id, student_answer, score, max_score) VALUES (1, 5, '300000000', 8, 10);"
    ]

    # Seed mistake analyses
    mistakes = [
        "INSERT INTO mistake_analysis (student_answer_id, mistake_type, feedback_text) VALUES (2, 'Formulefout', 'Je hebt de verkeerde formule gebruikt voor de afgeleide.');",
        "INSERT INTO mistake_analysis (student_answer_id, mistake_type, feedback_text) VALUES (4, 'Afrondingsfout', 'Je hebt de integraalconstante C vergeten.');",
        "INSERT INTO mistake_analysis (student_answer_id, mistake_type, feedback_text) VALUES (5, 'Eenhedenfout', 'De snelheid van licht is exact 299792458 m/s, geen afronding.');"
    ]

    all_seeds = subjects + questions + answers + mistakes

    for seed_sql in all_seeds:
        try:
            result = execute_query(seed_sql)
            print(f"Seeded: {seed_sql[:50]}...")
        except Exception as e:
            print(f"Error seeding: {e}")

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        migrate_foutenanalyse()
        seed_foutenanalyse()
        print("Migration completed!")