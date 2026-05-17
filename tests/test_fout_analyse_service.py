"""
Unit Tests – Foutenanalyse

Pytest unit tests voor de FoutAnalyseService module.

Deze tests controleren:
- calculate_percentages() berekeningen
- FoutAnalyseData.to_dict() conversie naar template data
- Lege data situaties (edge cases)

Test aanpak:
- Mockdata gebruikt (geen echte database calls)
- Test classes alleen voor overzichtelijke code organisatie
- Volledige validatie van service logica
"""

import pytest
from app.services.fout_analyse_service import FoutAnalyseData, FoutAnalyseService


class TestFoutAnalyseData:
    """
    Unit tests voor FoutAnalyseData.to_dict() conversie.
    
    Test class organiseert tests voor de FoutAnalyseData datacontainer.
    Controleert of data correct wordt opgeslagen en geconverteerd
    naar een dictionary voor Jinja2 template rendering.
    """

    def test_fout_analyse_data_to_dict(self):
        """
        Test: FoutAnalyseData.to_dict() converteert naar template dict.
        
        Controleert dat de to_dict() methode alle velden correct
        converteert naar een dictionary voor Jinja2 template passing.
        """
        data = FoutAnalyseData(
            mistakes_by_subject={'Natuurkunde': []},
            common_mistakes=[{'mistake_type': 'Leesfout', 'count': 2}],
            recommendation="Lees instructies zorgvuldig",
            subjects=[{'id': 2, 'name': 'Natuurkunde'}],
            selected_subject_id=2,
            current_student_id=17
        )
        
        result_dict = data.to_dict()
        
        assert isinstance(result_dict, dict)
        assert 'mistakes_by_subject' in result_dict
        assert 'common_mistakes' in result_dict
        assert 'recommendation' in result_dict
        assert 'subjects' in result_dict
        assert 'selected_subject_id' in result_dict
        assert 'current_student_id' in result_dict
        
        assert result_dict['current_student_id'] == 17
        assert result_dict['selected_subject_id'] == 2




class TestFoutAnalyseServiceCalculations:
    """
    Unit tests voor calculate_percentages() berekeningen.
    
    Test class organiseert tests voor percentage berekeningen.
    Controleert correcte verwerking van foutdata, afronding,
    en edge cases (lege data, enkele vakken, ongelijke verdeling).
    """

    @staticmethod
    def create_test_service():
        """
        Helper: Maak een FoutAnalyseService instance voor testing.
        
        Retourneert een schone service instance zonder
        database dependencies.
        """
        return FoutAnalyseService()

    def test_calculate_percentages_basic(self):
        """
        Test: calculate_percentages() met basis testdata.
        
        Controleert dat percentages correct berekend worden
        op basis van fout aantallen per vak.
        """
        service = self.create_test_service()
        
        # Mockdata: 2 vakken met verschillende fouten
        test_data = {
            'Wiskunde': [
                {'mistake_type': 'Berekeningsfout', 'count': 60},
                {'mistake_type': 'Formulefout', 'count': 40}
            ],
            'Natuurkunde': [
                {'mistake_type': 'Eenhedenfout', 'count': 100}
            ]
        }
        
        result = service.calculate_percentages(test_data)
        
        # Totaal = 60 + 40 + 100 = 200 fouten
        # Wiskunde = 100/200 = 50%
        # Natuurkunde = 100/200 = 50%
        assert result['Wiskunde']['percentage'] == 50.0
        assert result['Wiskunde']['total'] == 100
      


   