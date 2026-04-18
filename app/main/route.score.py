"""
Score module voor Brain Boost - Object Georiënteerde Programmeerstijl

Dit bestand bevat de score dashboard route en de data-preparatie logica
voor de scorepagina, volledig opgebouwd volgens object-georiënteerde principes.
"""

# Importeer benodigde Flask hulpmiddelen en database helper
from flask import render_template, session, request
from app.db import execute_query
from app.main import bp


# ===== DATABASE SCHEMA KLASSE =====
# Deze klasse beheert alle database schema definities voor de score module
class ScoreDatabaseSchema:
    """
    Beheert de database schema definities voor score gerelateerde tabellen.

    Deze klasse centraliseert alle SQL definities en biedt methodes
    om tabellen aan te maken in de database.
    """

    # SQL definitie voor de score tabel met alle kolommen en constraints
    SCORE_TABLE_SQL = """
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

    def initialize_score_table(self):
        """
        Maakt de score tabel aan in de database indien deze nog niet bestaat.

        Returns:
            bool: True indien succesvol, False bij fouten
        """
        try:
            execute_query(self.SCORE_TABLE_SQL)
            return True
        except Exception as e:
            print(f"Fout bij aanmaken score tabel: {e}")
            return False


# ===== DATA MODELLEN =====
# Deze klassen vertegenwoordigen de data structuren die gebruikt worden

class SubjectScore:
    """
    Vertegenwoordigt een vak score met naam, cijfer en verandering.

    Deze klasse kapselt alle informatie over een enkel vak score in.
    """

    def __init__(self, name, score, change=0):
        """
        Initialiseert een nieuwe vak score.

        Args:
            name (str): Naam van het vak
            score (float): Het cijfer voor dit vak
            change (float): Verandering ten opzichte van vorige periode
        """
        self.name = name
        self.score = score
        self.change = change

    def to_dict(self):
        """
        Converteert het object naar een dictionary voor template gebruik.

        Returns:
            dict: Dictionary representatie van het vak score object
        """
        return {
            "name": self.name,
            "score": self.score,
            "change": self.change
        }


class DashboardData:
    """
    Bevat alle data die nodig is voor het score dashboard.

    Deze klasse bundelt alle informatie die naar de template wordt gestuurd.
    """

    def __init__(self, average_score=0, monthly_change=0, trend=None, subjects=None):
        """
        Initialiseert dashboard data.

        Args:
            average_score (float): Gemiddelde score over alle vakken
            monthly_change (float): Maandelijkse verandering in procenten
            trend (list): Lijst met trend waarden voor de grafiek
            subjects (list): Lijst met SubjectScore objecten
        """
        self.average_score = average_score
        self.monthly_change = monthly_change
        self.trend = trend or [0, 0, 0, 0, 0, 0]
        self.subjects = subjects or []

    def to_dict(self):
        """
        Converteert alle data naar dictionary formaat voor de template.

        Returns:
            dict: Complete dashboard data als dictionary
        """
        return {
            "average_score": self.average_score,
            "monthly_change": self.monthly_change,
            "trend": self.trend,
            "subjects": [subject.to_dict() for subject in self.subjects]
        }


# ===== BUSINESS LOGIC SERVICE =====
# Deze klasse bevat alle bedrijfslogica voor score berekeningen

class ScoreCalculationService:
    """
    Behandelt alle berekeningen gerelateerd aan scores en trends.

    Deze service klasse isoleert alle wiskundige operaties en
    data transformaties van de rest van de applicatie.
    """

    def calculate_average_score(self, scores):
        """
        Berekent het gemiddelde van een lijst met scores.

        Args:
            scores (list): Lijst met numerieke scores

        Returns:
            float: Gemiddelde score, afgerond op 1 decimaal
        """
        if not scores:
            return 0.0
        return round(sum(scores) / len(scores), 1)

    def normalize_score_display(self, raw_score):
        """
        Normaliseert een ruwe score naar weergave formaat (gedeeld door 10).

        Args:
            raw_score (float): Ruwe score uit database

        Returns:
            float: Genormaliseerde score voor weergave
        """
        return round(float(raw_score) / 10, 1)

    def prepare_trend_data(self, scores, max_points=6):
        """
        Bereidt trend data voor voor de grafiek.

        Args:
            scores (list): Lijst met scores
            max_points (int): Maximum aantal punten in trend

        Returns:
            list: Trend data lijst met juiste lengte
        """
        if not scores:
            return [0] * max_points

        # Neem alleen de laatste max_points scores
        trend = scores[-max_points:]

        # Vul aan met nullen indien nodig
        if len(trend) < max_points:
            trend = [0] * (max_points - len(trend)) + trend

        return trend


class ScoreDataService:
    """
    Service voor het ophalen en verwerken van score data uit de database.

    Deze klasse combineert database toegang met data transformatie
    volgens object-georiënteerde principes.
    """

    def __init__(self):
        """
        Initialiseert de data service met benodigde dependencies.
        """
        self.calculation_service = ScoreCalculationService()

    def fetch_raw_scores(self, user_id):
        """
        Haalt ruwe score data op uit de database.

        Args:
            user_id (int): ID van de gebruiker

        Returns:
            list: Lijst met database rijen, of lege lijst bij fouten
        """
        try:
            rows = execute_query(
                "SELECT onderwerp, score FROM resultaat WHERE leerling_id = ?",
                (user_id,)
            )
            return rows
        except Exception:
            # Retourneer lege lijst bij database fouten
            return []

    def process_scores_to_subjects(self, raw_rows):
        """
        Converteert database rijen naar SubjectScore objecten.

        Args:
            raw_rows (list): Database rijen met onderwerp en score

        Returns:
            list: Lijst met SubjectScore objecten
        """
        subjects = []
        scores_for_average = []

        for row in raw_rows:
            raw_score = float(row.get("score", 0))
            display_score = self.calculation_service.normalize_score_display(raw_score)

            subject = SubjectScore(
                name=row.get("onderwerp", "Onbekend"),
                score=display_score,
                change=0  # Voor nu geen verandering berekening
            )

            subjects.append(subject)
            scores_for_average.append(display_score)

        return subjects, scores_for_average

    def get_dashboard_data(self, user_id):
        """
        Haalt en verwerkt alle data voor het dashboard.

        Args:
            user_id (int): ID van de gebruiker

        Returns:
            DashboardData: Complete dashboard data object
        """
        # Haal ruwe data op
        raw_rows = self.fetch_raw_scores(user_id)

        # Verwerk naar subject objecten
        subjects, scores_for_average = self.process_scores_to_subjects(raw_rows)

        # Bereken gemiddelde
        average_score = self.calculation_service.calculate_average_score(scores_for_average)

        # Bereid trend data voor
        trend_data = self.calculation_service.prepare_trend_data(scores_for_average)

        # Maak dashboard data object
        dashboard_data = DashboardData(
            average_score=average_score,
            monthly_change=0,  # Voor nu geen maandelijkse verandering
            trend=trend_data,
            subjects=subjects
        )

        return dashboard_data


# ===== PRESENTATION CONTROLLER =====
# Deze klasse beheert de presentatie logica en HTTP responses

class UserResolver:
    """
    Beheert het oplossen van gebruiker IDs uit verschillende bronnen.

    Deze klasse centraliseert logica voor het bepalen welke gebruiker
    de huidige request betreft.
    """

    def resolve_user_id(self, user_id=None):
        """
        Bepaalt de gebruiker ID uit request parameters of sessie.

        Args:
            user_id (int, optional): Direct opgegeven gebruiker ID

        Returns:
            int: Opgeloste gebruiker ID
        """
        if user_id is None:
            user_id = request.args.get("user_id", type=int)

        if user_id is None:
            user_id = session.get("leerling_id", 1)

        return user_id


class ScoreDashboardController:
    """
    Hoofdcontroller voor het score dashboard.

    Deze klasse orkestreert alle componenten om een complete
    dashboard pagina te renderen.
    """

    def __init__(self):
        """
        Initialiseert de controller met alle benodigde services.
        """
        self.data_service = ScoreDataService()
        self.user_resolver = UserResolver()
        self.database_schema = ScoreDatabaseSchema()

    def render_dashboard(self, user_id=None):
        """
        Rendert de complete score dashboard pagina.

        Args:
            user_id (int, optional): Specifieke gebruiker ID

        Returns:
            str: Gerenderde HTML template
        """
        # Los gebruiker ID op
        resolved_user_id = self.user_resolver.resolve_user_id(user_id)

        # Haal dashboard data op
        dashboard_data = self.data_service.get_dashboard_data(resolved_user_id)

        # Converteer naar dictionary voor template
        template_data = dashboard_data.to_dict()

        # Render template
        return render_template("events/score.html", data=template_data)

    def initialize_database(self):
        """
        Initialiseert de database tabellen.

        Returns:
            bool: True indien succesvol
        """
        return self.database_schema.initialize_score_table()


# ===== APPLICATIE INSTANTIES =====
# Maak globale instanties van de services en controllers (lazy loading)

def get_score_database():
    """Lazy loading van de database schema manager."""
    if not hasattr(get_score_database, '_instance'):
        get_score_database._instance = ScoreDatabaseSchema()
    return get_score_database._instance

def get_score_data_service():
    """Lazy loading van de data service."""
    if not hasattr(get_score_data_service, '_instance'):
        get_score_data_service._instance = ScoreDataService()
    return get_score_data_service._instance

def get_score_controller():
    """Lazy loading van de hoofdcontroller."""
    if not hasattr(get_score_controller, '_instance'):
        get_score_controller._instance = ScoreDashboardController()
    return get_score_controller._instance


# ===== ROUTE DEFINITIES =====
# Flask routes die de controller methodes aanroepen

@bp.route("/score")
@bp.route("/score/<int:user_id>")
def score(user_id=None):
    """
    Hoofdroute voor het score dashboard.

    Deze route delegeert naar de controller voor het renderen
    van de complete dashboard pagina.
    """
    controller = get_score_controller()
    return controller.render_dashboard(user_id)


# ===== HULPFUNCTIES =====
# Globale functies voor backward compatibility

def init_score_table():
    """
    Initialiseert de score tabel (voor backward compatibility).

    Returns:
        bool: True indien succesvol
    """
    database = get_score_database()
    return database.initialize_score_table()

