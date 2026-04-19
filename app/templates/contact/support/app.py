@app.route('/contact')
def contact_page ():
    faqs_raw = db_session.execute("SELECT * FROM faq").fetchall()


