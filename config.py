#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: freezed <freezed@users.noreply.github.com> 2018-08-23
Version: 0.1
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

This file is part of [ocp7](http://github.com/freezed/ocp7/) project.

"""
from os import environ

PORT = 1664
# HOST = 'localhost'
HOST = '192.168.1.70'
# HOST = '192.168.46.64'
APP = {
    'NAME': 'GrandPy Bot, le papy-robot',
    'SRC': 'http://github.com/freezed/ocp7/',
    'DEBUG': True,
    'MAP_LINK': 'https://opentopomap.org/#map=17/{lat}/{lng}',
}
GOO_API = {
    'URL_GEO': 'https://maps.googleapis.com/maps/api/geocode/json',
    'URL_MAP': 'https://maps.googleapis.com/maps/api/staticmap',
    'KEY': environ['GOO_API_KEY'],
    'MAP_SIZE': (600,300),
    'COUNTRY': 'FR',
    'MIN_QUERY_LEN': 5,
}
WIK_API = {
    'ROOT_URL': 'https://fr.wikipedia.org/w/api.php',
    'PARAM_SEARCH': {
        'action':'query',
        'utf8':True,
        'format':'json',
        'list':'search',
    },
    'PARAM_EXTRAC': {
        'action':'query',
        'utf8':True,
        'format':'json',
        'prop':'extracts',
        'exlimit':1,
        'explaintext':True,
        # 'exsentences':3,
        'exsectionformat':'plain',
        'exintro':True,
    }
}
VIEW_DEFAULT_VARS = {
    'query': '… no query …',
    'dev_log': '… no dev_log …',
    'address': '… no address …',
    'text': '… no text …',
    'map_img_src': 'https://via.placeholder.com/{}x{}?text=no+map'.format(
        *GOO_API['MAP_SIZE']
    ),
    'name': APP['NAME'],
    'url': APP['SRC'],
    'map_link': '',
}
