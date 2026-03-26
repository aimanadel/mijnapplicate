from flask import render_template, session, redirect, url_for, request, flash
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import execute_query

from app.main import bp


def docent_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("role") != "docent" or not session.get("docent_id"):
            flash("Je moet ingelogd zijn als docent om deze pagina te bekijken.")
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return wrapper


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
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
            flash("Wachtwoord moet minimaal 6 karakters lang zijn.")
            return redirect(url_for("main.register"))

        try:
            password_hash = generate_password_hash(password)
            result = execute_query(
                "INSERT INTO docent (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            flash("Account aangemaakt! Je kunt nu inloggen.")
            return redirect(url_for("main.login"))
        except Exception as e:
            flash(f"Error: Username of email bestaat al.")
            return redirect(url_for("main.register"))

    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Vul username en wachtwoord in.")
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
                flash("Ongeldige username of wachtwoord.")
        except Exception as e:
            flash(f"Error: {str(e)}")

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("Je bent uitgelogd.")
    return redirect(url_for("main.index"))


@bp.route("/over-mij")
def about_me():
    return render_template("zelfportret.html")

@bp.route("/home")
def home():
    return render_template("home.html")

@bp.route("/leerlingen")
@docent_required
def leerlingen():
    leerlingen = execute_query("SELECT id, naam, klas FROM leerling")
    klassen = sorted(list(set([l["klas"] for l in leerlingen])))
    return render_template("leerlingen.html", leerlingen=leerlingen, klassen=klassen)


@bp.route("/leerling")
def leerling_redirect():
    return redirect(url_for('main.leerlingen'))

@bp.route("/foutenanalyse")
def foutenanalyse():
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
        percentage = round((data["totaal"] / totaal) * 100, 1)

        resultaat.append({
            "categorie": cat,
            "percentage": percentage,
            "details": data["details"]
        })

    if resultaat:
        grootste = max(resultaat, key=lambda x: x["percentage"])
        aanbeveling = f"Focus op {grootste['categorie']} - dit is je grootste uitdaging met {grootste['percentage']}%."
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

@bp.route("/oefenen-opgaven")
def oefenen_opgaven():
    return render_template("oefenen_opgaven.html")
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
        uitleg = f"De leerling scoort laag op {zwak_onderwerp}"
        advies = f"Oefen extra op {zwak_onderwerp}"
    else:
        uitleg = "De leerling presteert goed"
        advies = "Ga door met oefenen"

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