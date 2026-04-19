from flask import render_template, redirect, url_for
from app.db import execute_query
from app.contact import bp

class FAQ:
    def __init__(self, id, question, answer):
        self.id = id
        self.question = question
        self.answer = answer

@bp.route('/contact')
def contact():
    """Contact & Support pagina met veelgestelde vragen en hulp informatie."""
    try:
        faqs_raw = execute_query("SELECT id, question, answer FROM faq")
        faq_objects = [FAQ(f['id'], f['question'], f['answer']) for f in faqs_raw]
    except Exception:
        faq_objects = []

    return render_template('contact/support/contact.html', faq_list=faq_objects)

@bp.route('/support')
def support():
    """Support pagina - doorverwijzen naar contact pagina."""
    return redirect(url_for('contact.contact'))