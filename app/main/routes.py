"""
routes.py
Eenvoudige Flask routes voor login, leerlingen en detailpagina
"""

from flask import render_template, session, redirect, url_for, request, flash
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import execute_query
from app.main import bp


# =========================
# Decorator: login verplicht
# =========================
def docent_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("role") != "docent":
            flash("Log eerst in.")
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return wrapper


# =========================
# Home pagina
# =========================
@bp.route("/")
def index():
    return render_template("index.html")


# =========================
# Registratie
# =========================
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("password_confirm")

        if not username or not email or not password:
            flash("Vul alles in.")
            return redirect(url_for("main.register"))

        if password != confirm:
            flash("Wachtwoorden komen niet overeen.")
            return redirect(url_for("main.register"))

        if len(password) < 6:
            flash("Wachtwoord moet minimaal 6 tekens zijn.")
            return redirect(url_for("main.register"))

        try:
            password_hash = generate_password_hash(password)

            execute_query(
                "INSERT INTO docent (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )

            flash("Account aangemaakt! Log in.")
            return redirect(url_for("main.login"))

        except:
            flash("Gebruiker bestaat al.")
            return redirect(url_for("main.register"))

    return render_template("register.html")


# =========================
# Login
# =========================
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Vul gebruikersnaam en wachtwoord in.")
            return redirect(url_for("main.login"))

        docent = execute_query(
            "SELECT id, username, password_hash FROM docent WHERE username = ?",
            (username,)
        )

        if docent and check_password_hash(docent[0]["password_hash"], password):
            session["docent_id"] = docent[0]["id"]
            session["role"] = "docent"

            flash("Welkom!")
            return redirect(url_for("main.leerlingen"))

        else:
            flash("Onjuiste login.")
            return redirect(url_for("main.login"))

    return render_template("login.html")


# =========================
# Logout
# =========================
@bp.route("/logout")
def logout():
    session.clear()
    flash("Uitgelogd.")
    return redirect(url_for("main.index"))


# =========================
# Leerlingenlijst (protected)
# =========================
@bp.route("/leerlingen")
@docent_required
def leerlingen():
    leerlingen = execute_query("SELECT id, naam, klas FROM leerling")

    klassen = sorted(list(set([l["klas"] for l in leerlingen])))

    return render_template(
        "leerlingen.html",
        leerlingen=leerlingen,
        klassen=klassen
    )


# =========================
# Leerling detail (protected)
# =========================
@bp.route("/leerling/<int:leerling_id>")
@docent_required
def leerling_detail(leerling_id):
    leerling = execute_query(
        "SELECT * FROM leerling WHERE id = ?",
        (leerling_id,)
    )[0]

    resultaten = execute_query(
        "SELECT onderwerp, score FROM resultaat WHERE leerling_id = ?",
        (leerling_id,)
    )

    laagste_score = 100
    zwak_onderwerp = ""

    for r in resultaten:
        if r["score"] < laagste_score:
            laagste_score = r["score"]
            zwak_onderwerp = r["onderwerp"]

    if laagste_score < 50:
        advies = f"Oefen extra op {zwak_onderwerp}"
    else:
        advies = "Ga zo door!"

    return render_template(
        "leerlingdetail.html",
        leerling=leerling,
        resultaten=resultaten,
        advies=advies
    )