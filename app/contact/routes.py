from flask import render_template, redirect, url_for, request, flash
from app.db import execute_query
from app.contact import bp

class FAQ:
    def __init__(self, id, question, answer):
        self.id = id
        self.question = question
        self.answer = answer

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact & Support pagina met veelgestelde vragen en hulp informatie."""
    if request.method == 'POST':
        # Haal formulier data op
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Simpele validatie
        if not name or not email or not message:
            flash('Alle velden zijn verplicht.', 'danger')
            return redirect(url_for('contact.contact'))

        # Hier zou je normaal gesproken de data opslaan in de database
        # of een e-mail versturen. Voor nu geven we een succes bericht.
        flash(f'Bedankt {name}! Je bericht is verzonden. We nemen zo snel mogelijk contact met je op.', 'success')
        return redirect(url_for('contact.contact'))

    # GET request - toon de pagina
    try:
        faqs_raw = execute_query("SELECT id, question, answer FROM faq")
        faq_objects = [FAQ(f['id'], f['question'], f['answer']) for f in faqs_raw]
    except Exception as e:
        # Fallback naar statische FAQ data als de database tabel niet bestaat
        print(f"Database query failed: {e}")
        faq_objects = [
            FAQ(1, "Wat zijn de openingstijden?", "Wij zijn elke werkdag bereikbaar van 09:00 tot 17:00."),
            FAQ(2, "Hoe kan ik jullie bereiken?", "Je kunt ons mailen of het contactformulier hieronder invullen.")
        ]

    return render_template('contact/support/contact.html', faq_list=faq_objects)

@bp.route('/support')
def support():
    """Support pagina - doorverwijzen naar contact pagina."""
    return redirect(url_for('contact.contact'))