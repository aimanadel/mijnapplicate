"""
Score module voor Brain Boost.

Dit bestand bevat de score dashboard route en de data-preparatie logica
voor de scorepagina.
"""

# Importeer Flask hulpmiddelen en database helper.
from flask import render_template, session, request
from app.db import execute_query
from app.main import bp


class ScoreService:
    """
    Serviceobject voor het score dashboard.

    Deze klasse haalt scoregegevens uit de database en
    zet de gegevens om naar een vorm die de template kan gebruiken.
    """

    def get_dashboard_data(self, user_id):
        """
        Haalt scoregegevens op voor een leerling en berekent de waardes.
        """
        try:
            rows = execute_query(
                "SELECT onderwerp, score FROM resultaat WHERE leerling_id = ?",
                (user_id,)
            )
        except Exception:
            # Als er iets mis gaat met de database, gebruik dan een lege lijst.
            rows = []

        subjects = []
        trend = []

        # Verwerk elke rij uit de database naar de juiste weergave.
        for row in rows:
            raw_score = float(row.get("score", 0))
            display_score = round(raw_score / 10, 1)
            subjects.append({
                "name": row.get("onderwerp", "Onbekend"),
                "score": display_score,
                "change": 0
            })
            trend.append(display_score)

        # Bereken het gemiddelde of geef standaardwaarden.
        if subjects:
            average_score = round(sum(item["score"] for item in subjects) / len(subjects), 1)
        else:
            average_score = 0
            trend = [0, 0, 0, 0, 0, 0]

        # Houd maximaal zes trendwaarden over.
        trend = trend[-6:]
        if len(trend) < 6:
            trend = [0] * (6 - len(trend)) + trend

        return {
            "average_score": average_score,
            "monthly_change": 0,
            "trend": trend,
            "subjects": subjects,
        }


class ScoreController:
    """
    Controller voor de scorepagina.

    Deze klasse gebruikt ScoreService om de juiste data te krijgen
    en maakt daarna de HTML pagina klaar.
    """

    def __init__(self, service):
        self.service = service

    def resolve_user_id(self, user_id=None):
        """
        Bepaalt welke leerling-ID gebruikt moet worden.
        """
        if user_id is None:
            user_id = request.args.get("user_id", type=int)

        if user_id is None:
            user_id = session.get("leerling_id", 1)

        return user_id

    def render_score_page(self, user_id=None):
        """
        Maakt de data voor de scorepagina klaar en toont de template.
        """
        user_id = self.resolve_user_id(user_id)
        data = self.service.get_dashboard_data(user_id)
        return render_template("events/score.html", data=data)


# Maak instantie van de services en controller.
score_service = ScoreService()
score_controller = ScoreController(score_service)


@bp.route("/score")
@bp.route("/score/<int:user_id>")
def score(user_id=None):
    """
    Route voor de scorepagina.

    Deze functie geeft het verzoek door aan de controller.
    """
    return score_controller.render_score_page(user_id)

