class FAQ:
    """
    Representeert een veelgestelde vraag (Frequently Asked Question).
    Deze class wordt gebruikt om data uit de database te transformeren naar een object.
    """
def __init__(self, id, question, answer):
    """
        Initialiseert een nieuw FAQ object.
        :param id: De unieke identifier uit de database (int).
        :param question: De vraagtekst (str).
        :param answer: Het volledige antwoord (str).
        """
    self.id = id
    self.question = question
    self.answer = answer

def get_summary(self):
    """
        Geeft een samenvatting van het antwoord terug.
        :return: Een string van maximaal 50 karakters.
        """
    if len(self.answer) > 50:
            # Snijd de tekst af en voeg puntjes toe voor een nette weergave
            return self.answer[:50] + "..."
    return self.answer