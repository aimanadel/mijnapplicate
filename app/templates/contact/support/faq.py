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

class ContactMessage:
    """
    Representeert een door de gebruiker ingezonden contactbericht.
    Bevat logica voor data-validatie alvorens opslag in de database.
    """

    def __init__(self, name, email, message_text):
        """
        Initialiseert een ContactMessage object.
        :param name: Naam van de afzender (str).
        :param email: E-mailadres van de afzender (str).
        :param message_text: De inhoud van het bericht (str).
        """
        self.name = name
        self.email = email
        self.message_text = message_text

    def is_valid(self):
        """
        Controleert of de invoer voldoet aan de minimale eisen.
        :return: True als velden gevuld zijn en email een @ bevat, anders False.
        """
        if not self.name or not self.email or not self.message_text:
            return False
        return "@" in self.email