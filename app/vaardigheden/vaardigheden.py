class Vaardigheid:
    """
    Representeert een specifieke vaardigheid van een leerling.
    
    Deze class beheert zowel de data als de logica voor de visuele 
    weergave van scores en trends in de frontend.
    """
    def __init__(self, name, score, trend):
        """
        Initialiseert een nieuw Skill object.
         Functiedefinities:
            name (str): De naam van de vaardigheid.
            score (int): Een waarde van 1 t/m 5 die de beheersing aangeeft.
            trend (str): De voortgangstrend ('up', 'down', of 'stable').
        """
        self.name = name
        self.score = score
        self.trend = trend

    def get_stars(self):
        """
        Genereert een lijst van booleans om de sterren-rating te representeren.
        
        Dit wordt in de Jinja-template gebruikt om te bepalen of een ster 
        ingekleurd (True) of leeg (False) moet zijn.

        Returns:
            list: Een lijst van 5 booleans, bijv. [True, True, True, False, False] voor een score van 3.
        """
        # We maken een lijst aan door te controleren of de huidige positie (i)
        stars = []
        for i in range(1, 6):
            stars.append(i <= self.score)
        return stars

    def get_trend_icon(self):
        """ Vertaalt de trend-attribute naar een visueel tekst-symbool.
        Returns: Een symbool dat de trend richting aangeeft.
        """
        icons = {
            "up": "↑",  # Stijgende lijn
            "down": "↓",    # Dalende lijn
            "stable": "−"   # Gelijk gebleven
        }
        # .get() voorkomt errors als er een onverwachte waarde in self.trend staat
        return icons.get(self.trend, "−")
    