#!/usr/bin/env python3
"""Initialize the database with the schema."""

from app.db import execute_query

def init_db():
    """Execute the schema.sql to create tables."""
    with open('app/schema.sql', 'r') as f:
        schema = f.read()

    # Split by semicolon, but handle multiline
    statements = [stmt.strip() for stmt in schema.split(';') if stmt.strip()]

    for stmt in statements:
        if stmt:
            print(f"Executing: {stmt[:50]}...")
            result = execute_query(stmt)
            print(f"Result: {result}")

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        init_db()