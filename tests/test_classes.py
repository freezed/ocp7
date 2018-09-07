import flasklocal.classes as script
import pytest

###############
#### PLACE ####
###############

class TestPlace:
    TXTINPUT = "Salut GrandPy! Est-ce que tu connais l'adresse d'OpenClassrooms ?"
    PLACE = script.Place(TXTINPUT)

    def test_get_query(self):
        assert self.PLACE.query == self.TXTINPUT

    def test_geo_data_type(self):
        assert isinstance(self.PLACE.geo_data, dict)

    def test_article_data_type(self):
        assert isinstance(self.PLACE.article_data, dict)

    def test_compare(self):
        assert self.PLACE.compare(self.TXTINPUT) == "salut grandpy! est ce que tu connais l adresse d openclassrooms ?"



###############
#### QUERY ####
###############

class TestQuery:
    QUERY = script.Query(
        "Salut GrandPy! Est-ce que tu connais l'adresse d'OpenClassrooms ?"
    )

    def test_get_textinput(self):
        assert self.QUERY._textinput_cf == "salut grandpy! est-ce que tu connais l'adresse d'openclassrooms ?"

    def test_textinput_type(self):
        assert isinstance(self.QUERY._textinput_cf, str)

    def test_stop_type(self):
        assert isinstance(self.QUERY.stop, list)

    def test_parser(self):
        self.QUERY.parse()
        assert self.QUERY.in_string == "openclassrooms"
