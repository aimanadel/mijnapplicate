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
    leerling_id = 1  # test (later dynamisch maken)

    query = "SELECT type, aantal FROM fout WHERE leerling_id = %s"
    fouten = execute_query(query, (leerling_id,))

    return render_template("foutenanalyse.html", fouten=fouten)