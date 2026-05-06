from flask import render_template, session, redirect, url_for, request, flash, jsonify
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import execute_query
import json
from app.main import bp
from .error_analyzer import ErrorAnalyzer





@bp.route("/")
def index():
    """
    Homepage - Redirect naar dashboard.
    """
    return redirect(url_for('main.home'))




@bp.route("/over-mij")
def about_me():
    """
    About pagina.
    """
    return render_template("zelfportret.html")

@bp.route("/home")
def home():
    try:
        leerling_id = session.get("leerling_id", 1)

        # 🔴 Foutenanalyse ophalen
        try:
            analyzer = ErrorAnalyzer(leerling_id)
            analyzer.analyze()
            data = analyzer.get_data()
            fouten = data.get("fouten", [])
            aanbeveling = data.get("aanbeveling", "Blijf oefenen!")
        except Exception as e:
            print(f"⚠️ Fout bij ErrorAnalyzer: {e}")
            fouten = []
            aanbeveling = "Oefenen maakt perfect!"

        # 🟣 Skills (kan later uit database)
        skills = [
            {"name": "Tijdsbeheer", "score": 4, "trend": "up"},
            {"name": "Concentratie", "score": 3, "trend": "flat"},
            {"name": "Nauwkeurigheid", "score": 4, "trend": "up"},
            {"name": "Probleemoplossend", "score": 5, "trend": "up"},
        ]

        # 🔵 Gemiddelde score berekenen
        if fouten:
            gemiddelde_score = round(
                10 - (sum(f["percentage"] for f in fouten) / len(fouten)) / 10, 1
            )
        else:
            gemiddelde_score = 7.4

        # 📈 Dummy trend (later uit DB)
        trend_scores = [6, 6.5, 6.2, 7]

        user = {
            "name": session.get("user", "Jouw Naam"),
            "initials": "JN"
        }

        return render_template(
            "home.html",
            fouten=fouten[:3],
            aanbeveling=aanbeveling,
            skills=skills,
            gemiddelde_score=gemiddelde_score,
            trend_scores=trend_scores,
            user=user
        )
    except Exception as e:
        print(f"❌ Fout in home route: {e}")
        flash(f"Fout: {str(e)}", "error")
        return redirect(url_for('main.index'))


@bp.route("/leerlingen")
def leerlingen():
    """
    Overzicht van alle leerlingen.
    """
    leerlingen = execute_query("SELECT id, naam, klas FROM leerling")
    klassen = sorted({l.get("klas") for l in leerlingen if l.get("klas") is not None})
    
    return render_template(
        "leerlingen.html",
        leerlingen=leerlingen,
        klassen=klassen
    )


@bp.route("/leerling")
def leerling_redirect():
    """
    Redirect naar overzicht als geen ID is opgegeven.
    """
    return redirect(url_for('main.leerlingen'))


# Aanbevelingen pagina route

@bp.route("/aanbevelingen")
def aanbevelingen():
    """Render the recommendations page for students with tips."""

    menu_items = [
        {"name": "Dashboard", "url": url_for('main.index'), "active": False},
        {"name": "Aanbevelingen", "url": url_for('main.aanbevelingen'), "active": True},
    ]

    user = {
        "name": session.get("user", "Gast"),
        "role": session.get("role", "leerling")
    }

    try:
        exercises = execute_query("SELECT id, title, description, duration FROM exercises")
    except Exception:
        exercises = []

    cards = []
    for e in exercises:
        if not isinstance(e, dict):
            continue

        cards.append({
            "title": e.get("title", "Onbekend"),
            "description": e.get("description", "Geen beschrijving"),
            "time": e.get("duration", 10),
            "exercises": 10,
            "color": "primary"
        })

    if not cards:
        cards = [
            {"title": "Vermijd Haastige Conclusies", "description": "Lees alle antwoordopties goed voordat je kiest.", "time": 15, "exercises": 12, "color": "red"},
            {"title": "Sleutelwoorden Herkennen", "description": "Oefen met markeren van belangrijke woorden.", "time": 10, "exercises": 8, "color": "purple"},
            {"title": "Tijdsplanning Verbeteren", "description": "Leer beter je tijd in delen zodat je op tijd klaar bent.", "time": 20, "exercises": 15, "color": "blue"},
        ]

    completed = [
        {"title": "Concentratie Oefeningen", "score": 8.5},
        {"title": "Tijdsbeheer Basis", "score": 7.8},
    ]

    upcoming = [
        {"title": "Nieuwe Oefeningen: Nauwkeurigheid"},
        {"title": "Nieuwe Oefeningen: Spelling"},
    ]

    return render_template(
        "events/aanbevelingen.html",
        menu_items=menu_items,
        subtitle="Persoonlijke oefeningen en aanbevelingen om te verbeteren",
        user=user,
        cards=cards,
        completed=completed,
        upcoming=upcoming,
        cta_text="Start nu met oefenen"
    )


@bp.route("/leerling/<int:leerling_id>")
def leerling_detail(leerling_id):
    """
    Detailpagina van één leerling.

    Bevat:
    - Basisgegevens
    - Resultaten
    - Foutenanalyse
    - Uitleg en advies
    """
    leerling = execute_query(
        "SELECT * FROM leerling WHERE id = ?",
        (leerling_id,)
    )[0]

    resultaten = execute_query(
        "SELECT onderwerp, score FROM resultaat WHERE leerling_id = ?",
        (leerling_id,)
    )

    fouten = execute_query(
        "SELECT categorie, subcategorie, aantal FROM fout WHERE leerling_id = ?",
        (leerling_id,)
    )

    categorieen = {}
    for fout in fouten:
        cat = fout["categorie"]
        categorieen.setdefault(cat, []).append(fout)

    laagste_score = 100
    zwak_onderwerp = ""
    
    for r in resultaten:
        if r["score"] < laagste_score:
            laagste_score = r["score"]
            zwak_onderwerp = r["onderwerp"]

    if laagste_score < 50:
        uitleg = f"Low score in {zwak_onderwerp}"
        advies = f"Practice extra on {zwak_onderwerp}"
    else:
        uitleg = "Student is performing well"
        advies = "Keep practicing"

    return render_template(
        "leerlingdetail.html",
        leerling=leerling,
        resultaten=resultaten,
        fouten=fouten,
        categorieen=categorieen,
        zwak_onderwerp=zwak_onderwerp,
        uitleg=uitleg,
        advies=advies
    )


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