from flask import render_template 
from app.db import execute_query

from app.main import bp


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/over-mij")
def about_me():
    return render_template("zelfportret.html")

@bp.route("/home")
def home():
    return render_template("home.html")
@bp.route ("/leerling")
def leerling():
    return render_template("leerling.html")

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
def leerling_detail(leerling_id):

    # leerling ophalen
    leerling = execute_query(
        "SELECT * FROM leerling WHERE id = ?",
        (leerling_id,)
    )[0]

    # resultaten ophalen
    resultaten = execute_query(
        "SELECT onderwerp, score FROM resultaat WHERE leerling_id = ?",
        (leerling_id,)
    )

    # zwakste onderwerp bepalen
    laagste_score = 100
    zwak_onderwerp = ""

    for r in resultaten:
        if r["score"] < laagste_score:
            laagste_score = r["score"]
            zwak_onderwerp = r["onderwerp"]

    # simpele analyse
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
        zwak_onderwerp=zwak_onderwerp,
        uitleg=uitleg,
        advies=advies
    )