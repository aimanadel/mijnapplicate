from flask import render_template

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