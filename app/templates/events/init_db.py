import os
import sqlite3

def create_database(db_path='brainboost.db', sql_path='app/schema.sql'):
    """
    This function reads the SQL file and creates the actual database file.
    It sets up the exercises and result tables automatically.
    """

    connection = sqlite3.connect(db_path)
    with open(sql_path, 'r', encoding='utf-8') as f:
        connection.executescript(f.read())

    connection.commit()
    connection.close()


if __name__ == "__main__":
    # run from repository root: python app/templates/events/init_db.py
    create_database()