"""
Score module voor Brain Boost

Dit bestand heeft de route voor het score dashboard en haalt data op.
"""

from flask import render_template
from app.db import execute_query
from app.main import bp

ALLOWED_SUBJECTS = [
    'Wiskunde A',
    'Wiskunde B',
    'Wiskunde C',
    'Natuurkunde'
]
DEFAULT_USER_ID = 1

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

    def __init__(self, average_score=0, monthly_change=0, trend=None, subjects=None, error_message=None):
        self.average_score = average_score
        self.monthly_change = monthly_change
        self.trend = trend or [0, 0, 0, 0, 0, 0]
        self.subjects = subjects or []
        self.error_message = error_message

    def to_dict(self):
        return {
            "average_score": self.average_score,
            "monthly_change": self.monthly_change,
            "trend": self.trend,
            "subjects": [subject.to_dict() for subject in self.subjects],
            "error_message": self.error_message
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
            print(f"[score] resultaat rows for leerling_id={user_id}: {rows}")
        except Exception as exc:
            print(f"[score] SQL query error for leerling_id={user_id}: {exc}")
            return [], [], f"SQL query problem: {exc}"

        if not rows:
            return [], [], f"No database rows found for leerling_id={user_id}."

        raw_subjects = [row.get("onderwerp") for row in rows if row.get("onderwerp")]
        allowed_rows = [
            row for row in rows
            if row.get("onderwerp") in ALLOWED_SUBJECTS
        ]

        if not allowed_rows:
            found_subjects = sorted(set(raw_subjects))
            return [], [], (
                f"Found rows for leerling_id={user_id}, but no allowed subjects were found. "
                f"Found subjects: {found_subjects}. "
                f"Allowed subjects: {ALLOWED_SUBJECTS}."
            )

        allowed_rows.sort(key=lambda row: ALLOWED_SUBJECTS.index(row.get("onderwerp")))

        subjects = []
        scores_for_average = []

        for row in allowed_rows:
            raw_score = row.get("score", 0)
            try:
                raw_score = float(raw_score)
            except (TypeError, ValueError):
                raw_score = 0.0

            display_score = round(raw_score / 10, 1)

            subject = SubjectScore(
                name=row.get("onderwerp", "Onbekend"),
                score=display_score
            )
            subjects.append(subject)
            scores_for_average.append(display_score)

        return subjects, scores_for_average, None

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

    def get_dashboard_data(self, user_id=DEFAULT_USER_ID):
        """
        Haalt alle data voor dashboard.
        """
        subjects, scores, error_message = self.fetch_scores(user_id)
        average = self.calculate_average(scores)
        trend = self.prepare_trend(scores)

        return DashboardData(
            average_score=average,
            monthly_change=0,
            trend=trend,
            subjects=subjects,
            error_message=error_message
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
            user_id = DEFAULT_USER_ID

        data = self.service.get_dashboard_data(user_id)
        return render_template("events/score.html", data=data.to_dict())

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


