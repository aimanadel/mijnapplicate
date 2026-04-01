"""
Module: routes.py

Bevat alle Flask routes voor de ANSW student-analytics applicatie.

Functionaliteit:
- Authenticatie (login, register, logout)
- Overzicht van leerlingen
- Detailpagina per leerling
- Foutenanalyse
- Oefenpagina’s
- Beveiliging via @docent_required decorator

Afhankelijkheden:
- Flask
- werkzeug (password hashing)
- app.db (database queries)
"""

from flask import render_template, session, redirect, url_for, request, flash, jsonify
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import execute_query
import json
from app.main import bp


def docent_required(f):
    """
    Decorator: alleen toegankelijk voor ingelogde docenten.

    Werking:
    - Controleert session op docent_id en role
    - Redirect naar login indien niet ingelogd
    - Voert functie uit indien toegestaan
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("role") != "docent" or not session.get("docent_id"):
            flash("U moet ingelogd zijn als docent om deze pagina te bekijken.")
            return redirect(url_for("main.login"))
        
        return f(*args, **kwargs)
    
    return wrapper


@bp.route("/")
def index():
    """
    Homepage (geen login vereist).
    """
    return render_template("index.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Registration from new teacher 
    """
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        password_confirm = request.form.get("password_confirm", "")

        if not username or not email or not password:
            flash("Vul alle velden in.")
            return redirect(url_for("main.register"))

        if password != password_confirm:
            flash("Wachtwoorden komen niet overeen.")
            return redirect(url_for("main.register"))

        if len(password) < 6:
            flash("Wachtwoord moet minimaal 6 tekens bevatten.")
            return redirect(url_for("main.register"))

        try:
            password_hash = generate_password_hash(password)

            execute_query(
                "INSERT INTO docent (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )

            flash("Account aangemaakt! U kunt nu inloggen.")
            return redirect(url_for("main.login"))
        
        except Exception:
            flash("Fout: gebruikersnaam of e-mail bestaat al.")
            return redirect(url_for("main.register"))

    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Login for teachers.
    """
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Voer gebruikersnaam en wachtwoord in.")
            return redirect(url_for("main.login"))

        try:
            docent = execute_query(
                "SELECT id, username, password_hash FROM docent WHERE username = ?",
                (username,)
            )

            if docent and check_password_hash(docent[0]["password_hash"], password):
                session["docent_id"] = docent[0]["id"]
                session["user"] = docent[0]["username"]
                session["role"] = "docent"
                
                flash(f"Welkom, {username}!")
                return redirect(url_for("main.leerlingen"))
            else:
                flash("Ongeldige gebruikersnaam of wachtwoord.")
        
        except Exception as e:
            flash(f"Fout: {str(e)}")

    return render_template("login.html")


@bp.route("/logout")
def logout():
    """
    Logout en sessie reset.
    """
    session.clear()
    flash("U bent uitgelogd.")
    return redirect(url_for("main.index"))


@bp.route("/over-mij")
def about_me():
    """
    About pagina.
    """
    return render_template("zelfportret.html")


@bp.route("/home")
def home():
    """
    Home page.
    """
    return render_template("home.html")


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


@bp.route("/foutenanalyse")
def foutenanalyse():
    """
    Foutenanalyse van een leerling (demo: leerling_id=1).

    Werking:
    - Haalt fouten op
    - Groepeert per categorie
    - Berekent percentages
    - Genereert advies
    """
    leerling_id = 1

    query = """
    SELECT categorie, subcategorie, aantal
    FROM fout
    WHERE leerling_id = ?
    """

    fouten = execute_query(query, (leerling_id,))

    totaal = sum(f["aantal"] for f in fouten)

    categorieen = {}
    for fout in fouten:
        cat = fout["categorie"]
        
        if cat not in categorieen:
            categorieen[cat] = {
                "totaal": 0,
                "details": []
            }
        
        categorieen[cat]["totaal"] += fout["aantal"]
        categorieen[cat]["details"].append({
            "naam": fout["subcategorie"],
            "aantal": fout["aantal"]
        })

    resultaat = []
    for cat, data in categorieen.items():
        percentage = round((data["totaal"] / totaal) * 100, 1) if totaal > 0 else 0
        
        resultaat.append({
            "categorie": cat,
            "percentage": percentage,
            "details": data["details"]
        })

    if resultaat:
        grootste = max(resultaat, key=lambda x: x["percentage"])
        aanbeveling = f"Focus op {grootste['categorie']} ({grootste['percentage']}%)."
        
        labels = [item["categorie"] for item in resultaat]
        waarden = [item["percentage"] for item in resultaat]
    else:
        aanbeveling = "Geen fouten gevonden."
        labels = []
        waarden = []

    return render_template(
        "foutenanalyse.html",
        fouten=resultaat,
        aanbeveling=aanbeveling,
        labels=labels,
        waarden=waarden
    )


# Aanbevelingen pagina route

@bp.route("/aanbevelingen")
def aanbevelingen():
    """Render the recommendations page for students with tips and oefenopgaven."""

    menu_items = [
        {"name": "Dashboard", "url": url_for('main.index'), "active": False},
        {"name": "Aanbevelingen", "url": url_for('main.aanbevelingen'), "active": True},
        {"name": "Oefenen", "url": url_for('main.oefenen_opgaven'), "active": False},
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


     

