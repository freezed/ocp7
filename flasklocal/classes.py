#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: freezed <freezed@users.noreply.github.com> 2018-08-25
Version: 0.1
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

This file is part of [ocp7](http://github.com/freezed/ocp7/) project.

 """
import requests
from config import GOO_API, WIK_API


class Place:
    """
    Defines a place with the user query

    Gets geo data from Google geocode & static map API
    Gets information from Wikipedia API

    """

    def __init__(self, query):
        """
        Sets arguments
        """
        self.query = str(query)
        self.geo_data = {'status': False}
        self.article_data = {'status': False}

        # Get geodata
        if len(self.query) > GOO_API['MIN_QUERY_LEN']:
            self.set_geo_data()
            self.set_article_data()

    @staticmethod
    def compare(string):
        """ Returns a comparable version of string """
        return str(string).replace("-", " ").replace("'", " ").casefold()

    @staticmethod
    def get_json(url, payload):
        """
        Request API
        """
        response = requests.get(url, payload)
        api_json = response.json()

        if response.status_code == 200:
            return api_json

        else:
            return False

    def set_article_data(self):
        """
        Function documentation

        """
        payload = {'srsearch': self.query}
        # Adds basic API call parameters
        payload.update(**WIK_API['PARAM_SEARCH'])

        search_json = self.get_json(WIK_API['ROOT_URL'], payload)

        try:
            self.article_data['title'] = search_json['query']['search'][0]['title']
            self.article_data['pageid'] = search_json['query']['search'][0]['pageid']

        except KeyError:
            self.article_data['context'] = 'search KeyError'
            self.article_data['status'] = False

        except TypeError:
            self.article_data['context'] = 'search TypeError'
            self.article_data['status'] = False

        except IndexError:
            self.article_data['context'] = 'search IndexError'
            self.article_data['status'] = False

        else:
            self.article_data['status'] = True
            payload = {'titles': self.article_data['title']}
            # Adds basic API call parameters
            payload.update(**WIK_API['PARAM_EXTRAC'])

            article_json = self.get_json(WIK_API['ROOT_URL'], payload)

            try:
                self.article_data['extract'] = article_json['query']['pages'][str(self.article_data['pageid'])]['extract']

            except TypeError:
                self.article_data['context'] = 'article'
                self.article_data['status'] = False

    def set_geo_data(self):
        """
        Calls Google geocode API with a string query & retrieve a Place

        Filter API's JSON to keep only useful data
        """
        # Build URL request
        payload = {
            'key': GOO_API['KEY'],
            'address': self.query,
            'region': GOO_API['COUNTRY'],
            'country': GOO_API['COUNTRY'],
        }

        geo_json = self.get_json(GOO_API['URL_GEO'], payload)
        self.geo_data['status'] = True
        self.geo_data['truncated_address'] = {}

        for component in geo_json['results'][0]['address_components']:
            self.geo_data['truncated_address'].update(
                {component['types'][0]: component['long_name']}
            )

        try:
            self.geo_data['formatted_address'] = geo_json['results'][0]['formatted_address']
            self.geo_data['location'] = geo_json['results'][0]['geometry']['location']

        except TypeError:
            self.geo_data = {'error': 'no_data'}

        else:
            # No data if request ĥas less or more 1 result
            if len(geo_json['results']) > 1:
                self.geo_data['warning'] = 'no_single_geocode_result'

            elif not geo_json['results']:
                self.geo_data = {'error': 'no_geocode_result'}

            # Adds locality in orginal query if missing for more appropriateness
            try:
                if self.compare(self.geo_data['truncated_address']['locality'])\
                not in self.compare(self.query):
                    self.query = "{} {}".format(
                        self.query,
                        self.geo_data['truncated_address']['locality']
                    )

            except KeyError:
                self.geo_data['query_update_exception'] = 'locality'

    def get_map_src(self):
        """
        Return url of a static maps using Google Static Maps API
        """
        coord = "{},{}".format(
            self.geo_data['location']['lat'],
            self.geo_data['location']['lng'],
        )

        payload = {
            'center': coord,
            'markers': coord,
            'size': "{}x{}".format(*GOO_API['MAP_SIZE']),
        }

        response = requests.get(
            GOO_API['URL_MAP'],
            payload,
        )

        return response.url


class Query():
    """ Class doc """

    def __init__(self, textinput):
        """ Class initialiser """

        ask = ['connais', 'cherche', 'sais', 'penses', 'quoi', 'dis', 'entendu', 'parlé', 'est-ce']
        hello = ['hello', 'salut', 'bonjour', 'coucou', 'salutations', 'grandpy', 'pépé', 'papi', 'papy']
        key = ['adresse', 'rue', 'endroit', 'lieu', 'place', 'coordonnées']
        self.stop = ["a", "abord", "absolument", "afin", "ah", "ai", "aie", "ailleurs", "ainsi", "ait", "allaient", "allo", "allons", "allô", "alors", "anterieur", "anterieure", "anterieures", "apres", "après", "as", "assez", "attendu", "au", "aucun", "aucune", "aujourd", "aujourd'hui", "aupres", "auquel", "aura", "auraient", "aurait", "auront", "aussi", "autre", "autrefois", "autrement", "autres", "autrui", "aux", "auxquelles", "auxquels", "avaient", "avais", "avait", "avant", "avec", "avoir", "avons", "ayant", "b", "bah", "bas", "basee", "bat", "beau", "beaucoup", "bien", "bigre", "boum", "bravo", "brrr", "c", "car", "ce", "ceci", "cela", "celle", "celle-ci", "celle-là", "celles", "celles-ci", "celles-là", "celui", "celui-ci", "celui-là", "cent", "cependant", "certain", "certaine", "certaines", "certains", "certes", "ces", "cet", "cette", "ceux", "ceux-ci", "ceux-là", "chacun", "chacune", "chaque", "cher", "chers", "chez", "chiche", "chut", "chère", "chères", "ci", "cinq", "cinquantaine", "cinquante", "cinquantième", "cinquième", "clac", "clic", "combien", "comme", "comment", "comparable", "comparables", "compris", "concernant", "contre", "couic", "crac", "d", "da", "dans", "de", "debout", "dedans", "dehors", "deja", "delà", "depuis", "dernier", "derniere", "derriere", "derrière", "des", "desormais", "desquelles", "desquels", "dessous", "dessus", "deux", "deuxième", "deuxièmement", "devant", "devers", "devra", "different", "differentes", "differents", "différent", "différente", "différentes", "différents", "dire", "directe", "directement", "dit", "dite", "dits", "divers", "diverse", "diverses", "dix", "dix-huit", "dix-neuf", "dix-sept", "dixième", "doit", "doivent", "donc", "dont", "douze", "douzième", "dring", "du", "duquel", "durant", "dès", "désormais", "e", "effet", "egale", "egalement", "egales", "eh", "elle", "elle-même", "elles", "elles-mêmes", "en", "encore", "enfin", "entre", "envers", "environ", "es", "est", "et", "etant", "etc", "etre", "eu", "euh", "eux", "eux-mêmes", "exactement", "excepté", "extenso", "exterieur", "f", "fais", "faisaient", "faisant", "fait", "façon", "feront", "fi", "flac", "floc", "font", "g", "gens", "h", "ha", "hein", "hem", "hep", "hi", "ho", "holà", "hop", "hormis", "hors", "hou", "houp", "hue", "hui", "huit", "huitième", "hum", "hurrah", "hé", "hélas", "i", "il", "ils", "importe", "j", "je", "jusqu", "jusque", "juste", "k", "l", "la", "laisser", "laquelle", "las", "le", "lequel", "les", "lesquelles", "lesquels", "leur", "leurs", "longtemps", "lors", "lorsque", "lui", "lui-meme", "lui-même", "là", "lès", "m", "ma", "maint", "maintenant", "mais", "malgre", "malgré", "maximale", "me", "meme", "memes", "merci", "mes", "mien", "mienne", "miennes", "miens", "mille", "mince", "minimale", "moi", "moi-meme", "moi-même", "moindres", "moins", "mon", "moyennant", "multiple", "multiples", "même", "mêmes", "n", "na", "naturel", "naturelle", "naturelles", "ne", "neanmoins", "necessaire", "necessairement", "neuf", "neuvième", "ni", "nombreuses", "nombreux", "non", "nos", "notamment", "notre", "nous", "nous-mêmes", "nouveau", "nul", "néanmoins", "nôtre", "nôtres", "o", "oh", "ohé", "ollé", "olé", "on", "ont", "onze", "onzième", "ore", "ou", "ouf", "ouias", "oust", "ouste", "outre", "ouvert", "ouverte", "ouverts", "o|", "où", "p", "paf", "pan", "par", "parce", "parfois", "parle", "parlent", "parler", "parmi", "parseme", "partant", "particulier", "particulière", "particulièrement", "pas", "passé", "pendant", "pense", "permet", "personne", "peu", "peut", "peuvent", "peux", "pff", "pfft", "pfut", "pif", "pire", "plein", "plouf", "plus", "plusieurs", "plutôt", "possessif", "possessifs", "possible", "possibles", "pouah", "pour", "pourquoi", "pourrais", "pourrait", "pouvait", "prealable", "precisement", "premier", "première", "premièrement", "pres", "probable", "probante", "procedant", "proche", "près", "psitt", "pu", "puis", "puisque", "pur", "pure", "q", "qu", "quand", "quant", "quant-à-soi", "quanta", "quarante", "quatorze", "quatre", "quatre-vingt", "quatrième", "quatrièmement", "que", "quel", "quelconque", "quelle", "quelles", "quelqu'un", "quelque", "quelques", "quels", "qui", "quiconque", "quinze", "quoi", "quoique", "r", "rare", "rarement", "rares", "relative", "relativement", "remarquable", "rend", "rendre", "restant", "reste", "restent", "restrictif", "retour", "revoici", "revoilà", "rien", "s", "sa", "sacrebleu", "sait", "sans", "sapristi", "sauf", "se", "sein", "seize", "selon", "semblable", "semblaient", "semble", "semblent", "sent", "sept", "septième", "sera", "seraient", "serait", "seront", "ses", "seul", "seule", "seulement", "si", "sien", "sienne", "siennes", "siens", "sinon", "six", "sixième", "soi", "soi-même", "soit", "soixante", "son", "sont", "sous", "souvent", "specifique", "specifiques", "speculatif", "stop", "strictement", "subtiles", "suffisant", "suffisante", "suffit", "suis", "suit", "suivant", "suivante", "suivantes", "suivants", "suivre", "superpose", "sur", "surtout", "t", "ta", "tac", "tant", "tardive", "te", "tel", "telle", "tellement", "telles", "tels", "tenant", "tend", "tenir", "tente", "tes", "tic", "tien", "tienne", "tiennes", "tiens", "toc", "toi", "toi-même", "ton", "touchant", "toujours", "tous", "tout", "toute", "toutefois", "toutes", "treize", "trente", "tres", "trois", "troisième", "troisièmement", "trop", "très", "tsoin", "tsouin", "tu", "té", "u", "un", "une", "unes", "uniformement", "unique", "uniques", "uns", "v", "va", "vais", "vas", "vers", "via", "vif", "vifs", "vingt", "vivat", "vive", "vives", "vlan", "voici", "voilà", "vont", "vos", "votre", "vous", "vous-mêmes", "vu", "vé", "vôtre", "vôtres", "w", "x", "y", "z", "zut", "à", "â", "ça", "ès", "étaient", "étais", "était", "étant", "été", "être", "ô"]

        self.stop.extend(ask)
        self.stop.extend(hello)
        self.stop.extend(key)
        self._textinput_cf = str(textinput).casefold()

        self.in_string = str()

    def parse(self):
        """
        Function documentation
        """
        result = []
        notresult = []

        # DEVLOG login found stop words
        for word in self._textinput_cf.split():

            if word in self.stop:
                result.append(word)

        for word in self._textinput_cf.split():

            # word is not in stopword list
            if word not in self.stop:

                # search for single quote or hyphen in word
                squote_idx = word.find("'")

                # word contain single quote : split it after
                if squote_idx != -1:
                    squote_idx += 1

                    if word[squote_idx:] not in self.stop:
                        notresult.append(word[squote_idx:])

                # word contains alnum
                elif word.isalnum():
                    notresult.append(word)

                # cleanning word of other non-alnum character
                else:
                    cleaned_word = str()

                    for char in word:
                        if char.isalnum() or char == "-":
                            cleaned_word += char

                    if cleaned_word not in self.stop:
                        notresult.append(cleaned_word)

        self.in_string = " ".join(notresult)

        return "text : «{}»\nresult : «{}»\nnotresult : «{}»".format(self._textinput_cf, result, notresult)
