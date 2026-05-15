"""
Foutanalyse module voor Brain Boost

Dit bestand bevat alle logica voor het foutenanalyse dashboard.
De service haalt data op uit de database en berekent foutstatistieken.
"""

from app.db import execute_query
from flask import render_template


# DEFINITIE: FOUTENANALYSE DATA KLASSE
# Deze klasse bevat alle data die voor het foutenanalyse dashboard nodig is.
# Dit zorgt voor een schone weergave en makkelijke passing naar templates.
class FoutAnalyseData:
    """
    Container voor alle foutenanalyse data.
    """

    def __init__(self, mistakes_by_subject=None, common_mistakes=None,
                 recommendation="", subjects=None, selected_subject_id=None):
        self.mistakes_by_subject = mistakes_by_subject or {}
        self.common_mistakes = common_mistakes or []
        self.recommendation = recommendation
        self.subjects = subjects or []
        self.selected_subject_id = selected_subject_id

    def to_dict(self):
        """
        Zet alle data om naar een dictionary voor template passing.
        """
        return {
            'mistakes_by_subject': self.mistakes_by_subject,
            'common_mistakes': self.common_mistakes,
            'recommendation': self.recommendation,
            'subjects': self.subjects,
            'selected_subject_id': self.selected_subject_id
        }


# DEFINITIE: FOUTENANALYSE SERVICE KLASSE
# Deze service bevat alle logica voor het ophalen en berekenen van foutdata.
# De klasse communiceert met de database en bereikt alle berekeningen.
class FoutAnalyseService:
    """
    Service voor het analyseren van fouten van leerlingen.
    Bevat methodes voor het ophalen, groeperen en analyseren van foutdata.
    """

    def __init__(self):
        self.mistake_types = [
            'Berekeningsfout',
            'Formulefout',
            'Afrondingsfout',
            'Stappen ontbreken',
            'Leesfout',
            'Eenhedenfout',
            'Grafiekfout'
        ]

    # DEFINITIE: FOUTEN PER VAK OPHALEN
    # Deze methode haalt de fouten van een leerling op uit de database
    # en groepeert deze per vak. De uitkomst wordt gebruikt voor de grafiek
    # op de Foutenanalyse-pagina.
    def get_mistakes_by_subject(self, student_id):
        """
        Haalt alle fouten van een leerling op en groepeert ze per vak.

        Args:
            student_id (int): ID van de leerling

        Returns:
            dict: Dictionary met vakken als keys en lijsten van fouten als values
        """
        query = """
        SELECT s.name as subject_name, ma.mistake_type, COUNT(*) as count
        FROM mistake_analysis ma
        JOIN student_answer sa ON ma.student_answer_id = sa.id
        JOIN question q ON sa.question_id = q.id
        JOIN subject s ON q.subject_id = s.id
        WHERE sa.student_id = ?
        GROUP BY s.name, ma.mistake_type
        ORDER BY s.name, count DESC
        """
        results = execute_query(query, (student_id,))

        mistakes_by_subject = {}
        for row in results:
            subject = row['subject_name']
            if subject not in mistakes_by_subject:
                mistakes_by_subject[subject] = []
            mistakes_by_subject[subject].append({
                'mistake_type': row['mistake_type'],
                'count': row['count']
            })

        return mistakes_by_subject

    
