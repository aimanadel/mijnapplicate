/*
BrainBoost - Score Module (Single File Version)

Deze module bevat alles voor het scoresysteem:
- Database model (Score)
- Service layer (business logic)
- Flask route (controller)

Het is opgebouwd volgens OOP principes (scheiding van verantwoordelijkheden).
*/

from flask import render_template
from app.main import bp
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# ==============================
# DATABASE SETUP (MODEL)
# ==============================

db = SQLAlchemy()

class Score(db.Model):
    """
    Model: Score
    Slaat scores op per gebruiker en per vak.
    """

    _tablename_ = "scores"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())



# ==============================
# SERVICE LAYER (OOP BUSINESS LOGIC)
# ==============================

class ScoreService:
    """
    Service Layer:
    Bevat alle logica voor het ophalen en berekenen van scores.
    """

    def get_dashboard_data(self, user_id):
        """
        Haalt alle data op voor het dashboard van één gebruiker.
        """

   # Alle scores ophalen uit database
        scores = Score.query.filter_by(user_id=user_id).all()

        # Gemiddelde score berekenen
        avg = (
            db.session.query(func.avg(Score.score))
            .filter(Score.user_id == user_id)
            .scalar()
        )
