from flask import render_template, request, redirect, url_for, session
from app.db import execute_query
from app.main import bp
from .error_analyzer import ErrorAnalyzer


@bp.route("/foutenanalyse")
@bp.route("/foutenanalyse/<int:leerling_id>")
def foutenanalyse(leerling_id=None):
    """
    Foutenanalyse van een leerling.

    Werking:
    - Haalt fouten op
    - Groepeert per categorie
    - Berekent percentages
    - Genereert advies
    
    Kan aangeroepen worden met leerling_id als URL parameter,
    of gebruikt de huidige ingelogde leerling.
    """
    # Als geen leerling_id wordt meegegeven, haal die op uit sessie
    if leerling_id is None:
        leerling_id = request.args.get("leerling_id", type=int)
    
    # Als nog steeds geen leerling_id, gebruik de sessie leerling
    if leerling_id is None:
        leerling_id = session.get("leerling_id", 1)
    
    analyzer = ErrorAnalyzer(leerling_id)
    analyzer.analyze()
    data = analyzer.get_data()

    return render_template(
        "foutenanalyse.html",
        fouten=data["fouten"],
        aanbeveling=data["aanbeveling"],
        labels=data["labels"],
        waarden=data["waarden"]
    )
