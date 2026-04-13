from flask import render_template, request, redirect, url_for, session
from app.db import execute_query
from app.main import bp


class ErrorData:
    """Representa uma linha de erro individual."""
    
    def __init__(self, categorie, subcategorie, aantal):
        self.categorie = categorie
        self.subcategorie = subcategorie
        self.aantal = aantal


class ErrorAnalyzer:
    """Analisa erros de um aluno e gera estatísticas."""
    
    def __init__(self, leerling_id):
        self.leerling_id = leerling_id
        self.raw_errors = []
        self.categorized_errors = {}
        self.result = []
        self.aanbeveling = ""
        self.labels = []
        self.waarden = []
    
    def fetch_errors_from_db(self):
        """Obtém os erros do banco de dados."""
        query = """
        SELECT categorie, subcategorie, aantal
        FROM fout
        WHERE leerling_id = ?
        """
        errors = execute_query(query, (self.leerling_id,))
        self.raw_errors = [ErrorData(**error) for error in errors]
    
    def get_total_errors(self):
        """Calcula o total de erros."""
        return sum(error.aantal for error in self.raw_errors)
    
    def categorize_errors(self):
        """Agrupa erros por categoria."""
        for error in self.raw_errors:
            if error.categorie not in self.categorized_errors:
                self.categorized_errors[error.categorie] = {
                    "totaal": 0,
                    "details": []
                }
            
            self.categorized_errors[error.categorie]["totaal"] += error.aantal
            self.categorized_errors[error.categorie]["details"].append({
                "naam": error.subcategorie,
                "aantal": error.aantal
            })
    
    def calculate_percentages(self):
        """Calcula percentuais para cada categoria."""
        totaal = self.get_total_errors()
        
        for categorie, data in self.categorized_errors.items():
            percentage = round((data["totaal"] / totaal) * 100, 1) if totaal > 0 else 0
            
            self.result.append({
                "categorie": categorie,
                "percentage": percentage,
                "details": data["details"]
            })
    
    def generate_recommendation(self):
        """Gera uma recomendação baseada na categoria com mais erros."""
        if self.result:
            biggest = max(self.result, key=lambda x: x["percentage"])
            self.aanbeveling = f"Focus op {biggest['categorie']} ({biggest['percentage']}%)."
            
            self.labels = [item["categorie"] for item in self.result]
            self.waarden = [item["percentage"] for item in self.result]
        else:
            self.aanbeveling = "Geen fouten gevonden."
            self.labels = []
            self.waarden = []
    
    def analyze(self):
        """Executa a análise completa."""
        self.fetch_errors_from_db()
        self.categorize_errors()
        self.calculate_percentages()
        self.generate_recommendation()
    
    def get_data(self):
        """Retorna os dados formatados para o template."""
        return {
            "fouten": self.result,
            "aanbeveling": self.aanbeveling,
            "labels": self.labels,
            "waarden": self.waarden
        }


@bp.route("/foutenanalyse")
@bp.route("/foutenanalyse/<int:leerling_id>")
def foutenanalyse(leerling_id=None):
    """
    Foutenanalyse van een leerling.

    Werking:
    - Haalt fouten op
    - Groepeert per categorie
    - Berekent percentages
    - Genereert advies
    
    Kan aangeroepen worden met leerling_id als URL parameter,
    of gebruikt de huidige ingelogde leerling.
    """
    # Als geen leerling_id wordt meegegeven, haal die op uit sessie
    if leerling_id is None:
        leerling_id = request.args.get("leerling_id", type=int)
    
    # Als nog steeds geen leerling_id, gebruik de sessie leerling
    if leerling_id is None:
        leerling_id = session.get("leerling_id", 1)
    
    analyzer = ErrorAnalyzer(leerling_id)
    analyzer.analyze()
    data = analyzer.get_data()

    return render_template(
        "foutenanalyse.html",
        fouten=data["fouten"],
        aanbeveling=data["aanbeveling"],
        labels=data["labels"],
        waarden=data["waarden"]
    )
