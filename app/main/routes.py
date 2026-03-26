"""
Module: routes.py
Author: [Your Name]
Purpose: Defines all Flask routes for the ANSW student-analytics system
Version: 1.0.0

Description:
This module contains all route handlers for authentication (login/register/logout),
student list overview, detail pages and error analysis. Also contains the
@docent_required decorator for route protection.

Dependencies:
  - Flask 3.0.3
  - werkzeug 3.0.2 (password hashing)
  - Custom: app.db module for database queries
"""

from flask import render_template, session, redirect, url_for, request, flash
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import execute_query

from app.main import bp


def docent_required(f):
    """
    Decorator: Requires docent login status to access protected routes.
    
    Simplified Flow:
      1. Check if session["role"] == "docent" AND session["docent_id"] exists
      2. If not: flash error message + redirect to login
      3. If yes: execute handler function normally
    
    Example usage:
      @bp.route("/leerlingen")
      @docent_required
      def leerlingen():
          # This is now protected
    
    Return:
      - Wrapper function (closure) that wraps the original function
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Validate docent login status in session
        if session.get("role") != "docent" or not session.get("docent_id"):
            flash("You must be logged in as a docent to view this page.")
            return redirect(url_for("main.login"))
        
        # Execute original route handler
        return f(*args, **kwargs)
    
    return wrapper


@bp.route("/")
def index():
    """
    Route: GET /
    Function: Application homepage
    
    Description:
      Shows the Welcome/Home page. No authentication required.
      This is the entry point for unauthenticated users.
    
    Return:
      - Rendered 'index.html' template
    
    Status codes:
      - 200: Success
    """
    return render_template("index.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Route: GET/POST /register
    Function: Create new teacher account
    
    Description:
      Registration form for new teachers. Accepts POST requests with
      username, email, password. Validates input and stores hashed password
      in docent table.
    
    POST Parameters (form):
      - username (str): Unique docent username (3-50 chars)
      - email (str): Email address (must be unique)
      - password (str): Password (min. 6 characters)
      - password_confirm (str): Password confirmation
    
    Validation steps:
      1. Check all fields are filled
      2. Check passwords match
      3. Check password length >= 6
      4. Hash password with werkzeug.security
      5. Insert into database (will fail if username/email already exists)
    
    Return:
      - GET: Rendered 'register.html' template
      - POST (success): Redirect to /login
      - POST (error): Redirect to /register with flash message
    
    Status codes:
      - 200: Form displayed
      - 302: Redirect (success or error)
    
    Database queries:
      INSERT INTO docent (username, email, password_hash) VALUES (?, ?, ?)
    
    Exception handling:
      - Catches duplicate key errors (username/email already exists)
    """
    if request.method == "POST":
        # === STEP 1: Gather and sanitize input ===
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        password_confirm = request.form.get("password_confirm", "")

        # === STEP 2: Validate required fields ===
        if not username or not email or not password:
            flash("Fill in all fields.")
            return redirect(url_for("main.register"))

        # === STEP 3: Check password match ===
        if password != password_confirm:
            flash("Passwords do not match.")
            return redirect(url_for("main.register"))

        # === STEP 4: Check password length ===
        if len(password) < 6:
            flash("Password must be at least 6 characters long.")
            return redirect(url_for("main.register"))

        # === STEP 5: Hash password and insert into DB ===
        try:
            # Generate bcrypt-style hash of password
            password_hash = generate_password_hash(password)
            
            # Insert new docent record
            result = execute_query(
                "INSERT INTO docent (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            
            flash("Account created! You can now log in.")
            return redirect(url_for("main.login"))
        
        except Exception as e:
            # Database constraint violation (username/email already in use)
            flash(f"Error: Username or email already exists.")
            return redirect(url_for("main.register"))

    # === GET request: Show registration form ===
    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Route: GET/POST /login
    Function: Teacher login to system
    
    Description:
      Authenticates teachers via username+password combination. Validates
      credentials against database and sets session variables if successful.
      This activates docent_required decorator protection for closed routes.
    
    POST Parameters (form):
      - username (str): Docent username
      - password (str): Unencrypted password (compare with hash)
    
    Authentication flow:
      1. Check both username and password are present
      2. Query docent table for username
      3. Use werkzeug check_password_hash() to verify password
      4. If match: set session["docent_id"], session["user"], session["role"]
      5. If no match: flash error, return to login form
    
    Return:
      - GET: Rendered 'login.html' form
      - POST (success): Redirect to /leerlingen (protected route)
      - POST (error): Redirect to /login with error message
    
    Status codes:
      - 200: Form displayed
      - 302: Redirect (success or error)
    
    Database queries:
      SELECT id, username, password_hash FROM docent WHERE username = ?
    
    Session variables (set on success):
      - session["docent_id"]: Unique docent ID (int)
      - session["user"]: Username (str)
      - session["role"]: "docent" (str) - used by @docent_required
    
    Security notes:
      - Passwords NEVER stored in plaintext
      - Uses werkzeug.security.check_password_hash (Bcrypt-style)
      - Generic error messages (don't say which field is wrong)
    
    Exception handling:
      - Database errors caught and flashed
    """
    if request.method == "POST":
        # === STEP 1: Gather input ===
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # === STEP 2: Validate presence ===
        if not username or not password:
            flash("Enter username and password.")
            return redirect(url_for("main.login"))

        # === STEP 3: Query docent in database ===
        try:
            docent = execute_query(
                "SELECT id, username, password_hash FROM docent WHERE username = ?",
                (username,)
            )

            # === STEP 4: Verify password hash ===
            if docent and check_password_hash(docent[0]["password_hash"], password):
                # Password correct! Set session variables
                session["docent_id"] = docent[0]["id"]
                session["user"] = docent[0]["username"]
                session["role"] = "docent"  # Used by @docent_required decorator
                
                flash(f"Welcome, {username}!")
                return redirect(url_for("main.leerlingen"))
            else:
                # Password wrong or user not found
                flash("Invalid username or password.")
        
        except Exception as e:
            # Unexpected database error
            flash(f"Error: {str(e)}")

    # === GET request: Show login form ===
    return render_template("login.html")


@bp.route("/logout")
def logout():
    """
    Route: GET /logout
    Function: Teacher logout from system
    
    Description:
      Removes all session variables (logout). Teacher can no longer access
      @docent_required protected routes.
    
    Return:
      - Redirect to / (homepage)
    
    Status codes:
      - 302: Redirect
    
    Session changes:
      - session.clear() clears ALL session data
    """
    # Clear all session information
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("main.index"))


@bp.route("/over-mij")
def about_me():
    """
    Route: GET /over-mij
    Function: Self-portrait/about page
    
    Return:
      - Rendered 'zelfportret.html' template
    """
    return render_template("zelfportret.html")


@bp.route("/home")
def home():
    """
    Route: GET /home
    Function: Home page
    
    Return:
      - Rendered 'home.html' template
    """
    return render_template("home.html")


@bp.route("/leerlingen")
@docent_required
def leerlingen():
    """
    Route: GET /leerlingen
    Function: Overview of all students (PROTECTED - docent-only)
    
    Description:
      Shows table of all students sorted by class.
      Template can filter by name and class via JavaScript.
      Requires @docent_required authorization.
    
    Return:
      - Rendered 'leerlingen.html' with:
        - leerlingen (list[dict]): All students with id, naam, klas
        - klassen (list[str]): Unique, sorted class list
    
    Status codes:
      - 200: Success (docent logged in)
      - 302: Redirect to login (not logged in)
    
    Database queries:
      SELECT id, naam, klas FROM leerling
    
    Template filters:
      - JavaScript real-time filter by name AND class
    """
    # === STEP 1: Query all students from database ===
    leerlingen = execute_query("SELECT id, naam, klas FROM leerling")
    
    # === STEP 2: Extract unique classes and sort ===
    klassen = sorted(list(set([l["klas"] for l in leerlingen])))
    
    return render_template(
        "leerlingen.html",
        leerlingen=leerlingen,
        klassen=klassen
    )


@bp.route("/leerling")
def leerling_redirect():
    """
    Route: GET /leerling
    Function: Fallback redirect (no specific student ID given)
    
    Description:
      Redirect to /leerlingen overview. Prevents 404 for /leerling URLs.
    
    Return:
      - Redirect to /leerlingen
    
    Status codes:
      - 302: Redirect
    """
    return redirect(url_for('main.leerlingen'))



@bp.route("/foutenanalyse")
def foutenanalyse():
    """
    Route: GET /foutenanalyse
    Function: Show error analysis diagram and recommendations
    
    Description:
      Analyzes student errors (hardcoded: leerling_id=1).
      Group errors by category, calculate percentages, generate advice.
      Data suitable for graphical display (labels + values for chart).
    
    Return:
      - Rendered 'foutenanalyse.html' with:
        - fouten (list[dict]): Groups with categorie, percentage, details[]
        - aanbeveling (str): Advice based on lowest score
        - labels (list[str]): Categories for X-axis chart
        - waarden (list[float]): Percentages for Y-axis chart
    
    Status codes:
      - 200: Success
    
    Database queries:
      SELECT categorie, subcategorie, aantal FROM fout WHERE leerling_id = ?
    
    Algorithm:
      1. Query all errors for student
      2. Group by category, sum count per category
      3. Calculate percentage of each category
      4. Identify highest percentage (biggest problem)
      5. Generate advice text
    
    Edge cases:
      - No errors: aanbeveling = "No errors found"
      - Empty lists: labels=[], waarden=[]
    
    Future improvements:
      - Replace hardcoded leerling_id=1 with parameter or session
      - Add date range filter
    """
    # === HARDCODED for demo: use leerling_id=1 ===
    leerling_id = 1

    # === STEP 1: Query errors for student ===
    query = """
    SELECT categorie, subcategorie, aantal
    FROM fout
    WHERE leerling_id = ?
    """
    fouten = execute_query(query, (leerling_id,))

    # === STEP 2: Calculate total errors ===
    totaal = sum(f["aantal"] for f in fouten)

    # === STEP 3: Group and aggregate by category ===
    categorieen = {}
    for fout in fouten:
        cat = fout["categorie"]
        
        # Initialize category if not yet present
        if cat not in categorieen:
            categorieen[cat] = {
                "totaal": 0,
                "details": []
            }
        
        # Add to total and append detail
        categorieen[cat]["totaal"] += fout["aantal"]
        categorieen[cat]["details"].append({
            "naam": fout["subcategorie"],
            "aantal": fout["aantal"]
        })

    # === STEP 4: Calculate percentages per category ===
    resultaat = []
    for cat, data in categorieen.items():
        percentage = round((data["totaal"] / totaal) * 100, 1) if totaal > 0 else 0
        
        resultaat.append({
            "categorie": cat,
            "percentage": percentage,
            "details": data["details"]
        })

    # === STEP 5: Generate advice and chart data ===
    if resultaat:
        # Identify category with highest percentage
        grootste = max(resultaat, key=lambda x: x["percentage"])
        aanbeveling = f"Focus on {grootste['categorie']} - this is your biggest challenge with {grootste['percentage']}%."
        
        # Extract data for chart (X=labels, Y=values)
        labels = [item["categorie"] for item in resultaat]
        waarden = [item["percentage"] for item in resultaat]
    else:
        # No errors found
        aanbeveling = "No errors found."
        labels = []
        waarden = []

    # === RENDER template met analyse data ===
    return render_template(
        "foutenanalyse.html",
        fouten=resultaat,
        aanbeveling=aanbeveling,
        labels=labels,
        waarden=waarden
    )


@bp.route("/oefenen-opgaven")
def oefenen_opgaven():
    """
    Route: GET /oefenen-opgaven
    Function: Show practice/exercise page
    
    Description:
      Practice exercises page. Currently placeholder template.
    
    Return:
      - Rendered 'oefenen_opgaven.html' template
    
    Status codes:
      - 200: Success
    """
    return render_template("oefenen_opgaven.html")


@bp.route("/leerling/<int:leerling_id>")
@docent_required
def leerling_detail(leerling_id):
    """
    Route: GET /leerling/<int:leerling_id>
    Function: Detail page of one student with performance analysis (PROTECTED)
    
    Description:
      Shows all student data: basic info, test results (scores),
      error analysis (error breakdown), and teacher-generated advice.
      Requires @docent_required authorization (docent-only).
    
    URL Parameters:
      - leerling_id (int): Unique student ID
    
    Return:
      - Rendered 'leerlingdetail.html' with following context:
        - leerling (dict): naam, klas, and other student attributes
        - resultaten (list[dict]): onderwerp, score for each test
        - fouten (list[dict]): categorie, subcategorie, aantal for each error
        - categorieen (dict): errors grouped by category
        - zwak_onderwerp (str): Subject with lowest score
        - uitleg (str): Human description of performance
        - advies (str): Teacher recommendation based on results
    
    Status codes:
      - 200: Success (docent logged in)
      - 302: Redirect to login (not logged in)
      - 500: If student not in database (IndexError on [0])
    
    Database queries:
      1. SELECT * FROM leerling WHERE id = ?
      2. SELECT onderwerp, score FROM resultaat WHERE leerling_id = ?
      3. SELECT categorie, subcategorie, aantal FROM fout WHERE leerling_id = ?
    
    Algorithm:
      1. Query student basic data from database
      2. Query scores for each test/subject
      3. Query errors/categories and counts
      4. Group errors by category
      5. Find subject with lowest score
      6. Generate advice based on lowest score:
         - score < 50: Practice extra on subject
         - score >= 50: Continue practicing
      7. Return combined data to template
    
    Template variables:
      - leerling: dict with naam="Jan Jansen", klas="6A"
      - resultaten: list<{onderwerp: "English", score: 78}>
      - categorieen: dict<categorie: [fout1, fout2, ...]>
      - zwak_onderwerp: "English" (lowest score)
      - uitleg: Human readable performance summary
      - advies: Teacher guidance text
    
    Security notes:
      - @docent_required decorator checks login status
      - Only logged-in teachers can access this route
    
    Edge cases:
      - IndexError if leerling_id doesn't exist (no try/catch!)
      - Empty lists: resultaten=[], fouten=[] (valid)
      - Division by zero: None (scores are always > 0)
    """
    # === STEP 1: Query student data ===
    leerling = execute_query(
        "SELECT * FROM leerling WHERE id = ?",
        (leerling_id,)
    )[0]  # Take first result; throws IndexError if not found

    # === STEP 2: Query test results (scores) ===
    resultaten = execute_query(
        "SELECT onderwerp, score FROM resultaat WHERE leerling_id = ?",
        (leerling_id,)
    )

    # === STEP 3: Query errors (errors) ===
    fouten = execute_query(
        "SELECT categorie, subcategorie, aantal FROM fout WHERE leerling_id = ?",
        (leerling_id,)
    )

    # === STEP 4: Group errors by category ===
    categorieen = {}
    for fout in fouten:
        cat = fout["categorie"]
        # Use setdefault for elegant initialization
        categorieen.setdefault(cat, []).append(fout)

    # === STEP 5: Find subject with lowest score ===
    laagste_score = 100
    zwak_onderwerp = ""
    
    for r in resultaten:
        if r["score"] < laagste_score:
            laagste_score = r["score"]
            zwak_onderwerp = r["onderwerp"]

    # === STEP 6: Generate explanation and advice ===
    if laagste_score < 50:
        # Score is below 50% - intervention needed
        uitleg = f"The student scores low on {zwak_onderwerp}"
        advies = f"Practice extra on {zwak_onderwerp}"
    else:
        # Score is OK - keep going
        uitleg = "The student is performing well"
        advies = "Keep practicing"

    # === RENDER template with complete analysis ====
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