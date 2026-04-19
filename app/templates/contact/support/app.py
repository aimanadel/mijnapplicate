from flask import render_template

@app.route('/contact')
def contact_page():
    # Haal de data op uit de database
    faqs_raw = db_session.execute("SELECT * FROM faq").fetchall()
    # Zet de data om naar OOP-objecten
    faq_objects = [FAQ(f.id, f.question, f.answer) for f in faqs_raw]
    # De return moet IN de functie staan (ingesprongen)
    return render_template('contact.html', faq_list=faq_objects)