"""
Score module voor Brain Boost

Dit bestand heeft de route voor het score dashboard en haalt data op.
"""

from flask import render_template, session, request
from app.db import execute_query
from app.main import bp

# Hier zijn de klassen voor de data die we gebruiken
# Dit is een klasse voor een vak score
class SubjectScore:
    """
    Een vak score met naam en cijfer.
    """

    def __init__(self, name, score, change=0):
        self.name = name
        self.score = score
        self.change = change

    def to_dict(self):
        return {
            "name": self.name,
            "score": self.score,
            "change": self.change
        }

# Dit is een klasse voor alle data van het dashboard
class DashboardData:
    """
    Alle data voor het dashboard.
    """

    def __init__(self, average_score=0, monthly_change=0, trend=None, subjects=None):
        self.average_score = average_score
        self.monthly_change = monthly_change
        self.trend = trend or [0, 0, 0, 0, 0, 0]
        self.subjects = subjects or []

    def to_dict(self):
        return {
            "average_score": self.average_score,
            "monthly_change": self.monthly_change,
            "trend": self.trend,
            "subjects": [subject.to_dict() for subject in self.subjects]
        }

# Hier is de service klasse voor scores
# Deze klasse haalt data op en doet berekeningen
class ScoreService:
    """
    Service voor scores ophalen en berekenen.
    """

    def fetch_scores(self, user_id):
        """
        Haalt scores op uit database.
        """
        try:
            rows = execute_query(
                "SELECT onderwerp, score FROM resultaat WHERE leerling_id = ?",
                (user_id,)
            )
        except Exception:
            rows = []

        subjects = []
        scores_for_average = []

        for row in rows:
            raw_score = float(row.get("score", 0))
            display_score = round(raw_score / 10, 1)

            subject = SubjectScore(
                name=row.get("onderwerp", "Onbekend"),
                score=display_score
            )
            subjects.append(subject)
            scores_for_average.append(display_score)

        return subjects, scores_for_average

    def calculate_average(self, scores):
        """
        Berekent gemiddelde.
        """
        return round(sum(scores) / len(scores), 1) if scores else 0.0

    def prepare_trend(self, scores, max_points=6):
        """
        Maakt trend data klaar.
        """
        if not scores:
            return [0] * max_points

        trend = scores[-max_points:]
        if len(trend) < max_points:
            trend = [0] * (max_points - len(trend)) + trend
        return trend

    def get_dashboard_data(self, user_id):
        """
        Haalt alle data voor dashboard.
        """
        subjects, scores = self.fetch_scores(user_id)
        average = self.calculate_average(scores)
        trend = self.prepare_trend(scores)

        return DashboardData(
            average_score=average,
            trend=trend,
            subjects=subjects
        )

# Hier is de controller voor het dashboard
# Deze zorgt voor de route en rendering
class ScoreController:
    """
    Controller voor score dashboard.
    """

    def __init__(self):
        self.service = ScoreService()

    def render_dashboard(self, user_id=None):
        """
        Rendert de dashboard pagina.
        """
        if user_id is None:
            user_id = request.args.get("user_id", type=int) or session.get("leerling_id", 1)

        data = self.service.get_dashboard_data(user_id)
        skills = [
            {"name": "Samenwerken", "score": 4, "trend": "up"},
            {"name": "Creativiteit", "score": 3, "trend": "stable"},
            {"name": "Probleemoplossen", "score": 5, "trend": "up"}
        ]
        return render_template("events/score.html", data=data.to_dict(), skills=skills)

# Maak een controller aan
controller = ScoreController()

# Hier zijn de routes voor Flask
@bp.route("/score")
@bp.route("/score/<int:user_id>")
def score(user_id=None):
    """
    Route voor score dashboard.
    """
    return controller.render_dashboard(user_id)

# Dit is een functie om de tabel aan te maken
def init_score_table():
    """
    Maakt score tabel aan.
    """
    sql = """
    CREATE TABLE `score` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `leerling_id` INT NOT NULL,
        `resultaat_id` INT,
        `gemiddelde_score` DECIMAL(5,2),
        `vorige_score` DECIMAL(5,2),
        `trend` VARCHAR(50),
        `periode` DATE,
        `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`leerling_id`) REFERENCES `leerling`(`id`) ON DELETE CASCADE,
        FOREIGN KEY (`resultaat_id`) REFERENCES `resultaat`(`id`) ON DELETE SET NULL,
        KEY `idx_leerling_id` (`leerling_id`),
        KEY `idx_periode` (`periode`),
        KEY `idx_leerling_periode` (`leerling_id`, `periode`)
    )
    """
    try:
        execute_query(sql)
        return True
    except Exception as e:
        print(f"Fout bij aanmaken score tabel: {e}")
        return False

