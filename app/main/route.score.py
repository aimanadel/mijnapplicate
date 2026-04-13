from flask import render_template

from app.main import bp


@bp.route("/score")
def score():
    """Render de score pagina."""
    return render_template("events/score.html")