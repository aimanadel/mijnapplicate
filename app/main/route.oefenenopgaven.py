from flask import render_template, request, jsonify
from app.db import execute_query
from app.main import bp
import json


@bp.route("/oefenen-opgaven")
def oefenen_opgaven():
    """
    Render de oefenopgaven-pagina.
    """
    return render_template("oefenen_opgaven.html")


def ensure_oefenopgaven_table():
    """
    Maakt de tabel aan als deze nog niet bestaat.
    """
    execute_query("""
        CREATE TABLE IF NOT EXISTS oefenopgaven_result (
            id INT NOT NULL AUTO_INCREMENT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            score INT NOT NULL,
            total_answered INT NOT NULL,
            incorrect_answers TEXT NOT NULL,
            PRIMARY KEY(id)
        )
    """)


def save_oefenopgaven(score, total_answered, incorrect_answers):
    """
    Slaat de resultaten op in de database.
    """
    ensure_oefenopgaven_table()

    execute_query(
        """
        INSERT INTO oefenopgaven_result (score, total_answered, incorrect_answers)
        VALUES (?, ?, ?)
        """,
        (score, total_answered, json.dumps(incorrect_answers, ensure_ascii=False))
    )


@bp.route("/oefenen-opgaven/resultaat", methods=["POST"])
def oefenen_opgaven_resultaat():
    """
    Ontvangt resultaten en slaat deze op.
    """
    data = request.get_json() or {}

    score = int(data.get("score", 0))
    total_answered = int(data.get("total_answered", 0))
    incorrect_answers = data.get("incorrect_answers", [])

    save_oefenopgaven(score, total_answered, incorrect_answers)

    return jsonify({"ok": True})
