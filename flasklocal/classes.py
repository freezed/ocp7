#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: freezed <freezed@users.noreply.github.com> 2018-08-25
Version: 0.1
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

This file is part of [ocp7](http://github.com/freezed/ocp7/) project.

 """
import urllib.parse as up
from pprint import pformat as pf
from random import choice as rc
import requests
from config import APP, GOO_API, WIK_API


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

    def trigger_api(self):
        # Get geodata
        if len(self.query) > GOO_API['MIN_QUERY_LEN']:
            self.set_geo_data()
        else:
            self.geo_data = {
                'status': False,
                'context': 'textinput too short',
            }

        if self.geo_data['status']:
            self.set_article_data()
        else:
            self.article_data['context'] = 'no geo_data'

    @staticmethod
    def compare(string):
        """ Returns a comparable version of string """
        return str(string).replace("-", " ").replace("'", " ").casefold()

    @staticmethod
    def get_json(url, payload):
        """
        Request API
        """
        try:
            response = requests.get(url, payload)
        except requests.exceptions.ConnectionError as except_detail:
            return {'ConnectionError': pf(except_detail)}

        try:
            api_json = response.json()
        except Exception as detail:
            return {
                'context': 'get_json() method',
                'error':{'JSONDecodeError': str(detail)}
            }
        else:
            if response.status_code == 200:
                return api_json

            else:
                return {
                    'context': 'get_json() method',
                    'error':{'status_code': response.status_code}
                }

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

        except KeyError as detail:
            self.article_data = {
                'status': False,
                'context': 'search article',
                'error': {
                    'KeyError': str(detail),
                    'response': search_json,
                }
            }

        except TypeError as detail:
            self.article_data = {
                'status': False,
                'context': 'search article',
                'error': {
                    'KeyError': str(detail),
                    'response': search_json,
                }
            }

        except IndexError as detail:
            self.article_data = {
                'status': False,
                'context': 'search article',
                'error': {
                    'KeyError': str(detail),
                    'response': search_json,
                }
            }

        else:
            self.article_data['status'] = True
            payload = {'titles': self.article_data['title']}
            # Adds basic API call parameters
            payload.update(**WIK_API['PARAM_EXTRAC'])

            article_json = self.get_json(WIK_API['ROOT_URL'], payload)

            try:
                self.article_data['extract'] = article_json['query']['pages'][str(self.article_data['pageid'])]['extract']

            except TypeError as detail:
                self.article_data = {
                    'status': False,
                    'context': 'article extract',
                    'error': {
                        'TypeError': str(detail),
                        'response': article_json,
                    }
                }

            except KeyError as detail:
                self.article_data = {
                    'status': False,
                    'context': 'article extract',
                    'error': {
                        'KeyError': str(detail),
                        'response': article_json,
                    }
                }

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

        try:
            for component in geo_json['results'][0]['address_components']:
                self.geo_data['truncated_address'].update(
                    {component['types'][0]: component['long_name']}
                )
            self.geo_data['formatted_address'] = geo_json['results'][0]['formatted_address']
            self.geo_data['location'] = geo_json['results'][0]['geometry']['location']

        except KeyError as detail:
            self.geo_data = {
                'status': False,
                'context': 'set_geo_data()',
                'error': {
                    'KeyError': str(detail),
                    'response': geo_json,
                }
            }

        except IndexError as detail:
            self.geo_data = {
                'status': False,
                'context': 'set_geo_data()',
                'error': {
                    'KeyError': str(detail),
                    'response': geo_json,
                }
            }

        except TypeError as detail:
            self.geo_data = {
                'status': False,
                'context': 'set_geo_data()',
                'error': {
                    'KeyError': str(detail),
                    'response': geo_json,
                }
            }

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
            'key': GOO_API['KEY'],
            'center': coord,
            'markers': coord,
            'size': "{}x{}".format(*GOO_API['MAP_SIZE']),
        }
        goo_url = up.urlparse(GOO_API['URL_MAP'])
        query = up.urlencode(payload)
        parts = (goo_url.scheme, goo_url.netloc, goo_url.path, '', query, '')

        return up.urlunparse(parts)


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
        notresult = []

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

        self.in_string = " ".join(notresult).strip()


class Message():
    """ Class doc """

    def __init__(self, place):
        """ Class initialiser """
        self.place = place
        self.babble = {
            'address_yes': [
                "Bien sûr mon poussin! Voici l'adresse",
                "Mais oui mon p'tit, tiens mon neurone vient de démarrer, voici l'adresse",
                "Oh oui, je m'en souviens bien, et hop, l'adresse",
                "Ouh, ça fait un bail! Mais si ma mémoire est bonne l'adresse est celle ci",
            ],
            'extract_yes': [
                "D'ailleurs j'ai passé un bout de temps dans le coin, laisse moi t'en causer un peu",
                "GrandMy (ma femme) adorait cet endroit, on y est allé souvent",
                "Là aussi on a passé de bons moments… Attends un peu que je te raconte",
                "J'y ai fais les 400 coups bien avant que tu mettes ta première couche-culotte",
            ],
            'address_no': [
                "Ça me dit rien gamin, reformule pour voir…",
                "Moi je gâtouille pas encore, par contre toi c'est moins sûr… Repose ta question!",
                "C'est pas très clair comme question, répète un peu…",
                "Nan mais j'suis pas prix Nobel moi!!",
            ],
            'extract_no': [
                "Euh, faut que je prenne mes pilules…",
                "Je t'ai dis que c'était l'heure de la sieste…",
                "Nan, mais j'ai déjà raconté cette histoire 100 fois!",
                "Et sinon, t'as pas des amis à qui causer?",
            ]
        }

    def address_no(self):
        return {'address': rc(self.babble['address_no']), 'map_link': False}

    def extract_no(self):
        return {'extract': rc(self.babble['extract_no']), 'curid': False}

    def address_yes(self):
        return {
            'map_img_src': self.place.get_map_src(),
            'map_link': APP['MAP_LINK'].format(**self.place.geo_data['location']),
            'address': "{} : {}".format(
                rc(self.babble['address_yes']),
                self.place.geo_data['formatted_address'],
            ),
        }

    def extract_yes(self):
        return {
            'curid': self.place.article_data['pageid'],
            'extract': "{} : {}………".format(
                rc(self.babble['extract_yes']),
                self.place.article_data['extract'][:200],
            )
        }
