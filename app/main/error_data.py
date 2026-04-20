class ErrorData:
    """Representa uma linha de erro individual."""

    def __init__(self, categorie, subcategorie, aantal):
        self.categorie = categorie
        self.subcategorie = subcategorie
        self.aantal = aantal