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

    
