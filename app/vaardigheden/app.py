from flask import Flask, render_template
from models.skill import Skill

app = Flask(__name__)

@app.route('/dashboard')
def dashboard():
    # Simulatie van data uit de database
    skills_data = [
        Skill("Python", 4, "up"),
        Skill("Flask", 3, "stable"),
        Skill("SQL", 2, "down")
    ]
    return render_template('dashboard.html', skills=skills_data)
