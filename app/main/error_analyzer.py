from app.db import execute_query
from .error_data import ErrorData


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