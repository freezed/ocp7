-[_Courses Open Classrooms_][oc]-

# [PyDev] Project 7

_Last version of this document is available on [gitlab][approach]._

## Approach

### Introduction

Get localisaton informations & _Wikipedia_ extracts about a place using a basic & user friendly tool with these caracteristics :

- mono-page website
- lone session : history disappear after a page refresh
- collecting user request and give response as a chat


This project was created for study purposes, to train with these tools :

- `REST APIs`
- [`flask`][flask] microframework
- `ECMAscript` & `AJAX`
- [Heroku][heroku] PaaS plateform


The whole exercise description is available on [OpenClassrooms site][oc], the project is hosted on [github][kanban] and it is deployed here : [https://ocp7-1664.herokuapp.com/](https://ocp7-1664.herokuapp.com/).


### Workflow

 - plan : features, scripts, files, functions, tools needed
 - create [features][features], grouped in autonomous packages
 - organize with a [_kanban type_ table][kanban ]
 - write tests with [`pytest`][pytest]
 - write code


### Code construction

To build the script, I followed this approach :

1. take in hand the necessary tools & play with it : [Gmaps][gmaps]/[Wiki Media][mediawiki] `API`, [Flask][flask], [pytest][pytest] & [Heroku][heroku]
    * choose API's needed (`geocode`, `static maps`, `list:search` & `prop:extracts`) and URLs
    * howto automated deploys on [Heroku][heroku]
    * choose the good tests
2. build a minimalistic [`Flask`][flask] app
3. build 1st tests on :
    * API response & data processing
    * scraper
4. code the scraper
5. exceptions catching
6. use HTML/CSS template
7. learn & use ECMAscript


### Code organization

```
├── config.py
├── doc              : Documentation
├── flasklocal       : Flask app content
│   ├── __init__.py
│   ├── classes.py   : Classes of the app
│   ├── static
│   │   ├── css
│   │   ├── img
│   │   └── js
│   ├── templates
│   └── views.py     : routes definition
├── Procfile         : Heroku's running config
├── run.py           : the app running script
└── tests            : pytest stuff
```

### Difficulties encountered

#### 1. How servers work

Flask built-in server, Gunicorn, Heroku's `Procfile`…

That was a bit messy and I needed time to get how these tools are working together (or not). This was a good occasion to start from scratch, building a [MCVE](https://stackoverflow.com/help/mcve) and by the way : post-it to a
[StackOverflow](https://stackoverflow.com/a/52005826/6709630) question without accepted answer.

#### 2. Discovering ECMAscript

I never used it before, so it took me a few days to get an overview of the possibilities I could use in this project. Started with the idea of using _jQuery library_ to do the job, I finally understand that _Vanilia JS_ could be a more efficient way to beginin with this language. In this quest I used various ressources : the [Moz://a Developper Network](https://developer.mozilla.org), Stack Overflow (of course…), and shared trails given by my OpenClassrooms's mentor & [Tonio](https://github.com/tonio) (an experimented friend).

#### 3. Try to catch them all

The exceptions of course. Building above 2 APIs, reserves the surprise of a number of unexpected responses. The goal was to never break the user experience and for that I had to build an efficient code structure to handle all unexpected situations.

#### 4. Stay in the scope

A good example is the server `loggin` job. The specifications do not mention it… but to track details of all the exceptions encountered I need some feedback. A nice way to do it would be using [_flask built-in logger_][log], but I fear for the time needed to handle it, so  I used a trivial way to do it.


### Possible [developments][issues]

* [Use Leaflet instead of 'gMaps static'][05]
* [Uses OSM Nominatim API][23]
* [Refactors parser code][26]
* [Adds WM requests and choose more pertinent response][36]
* [Exports app var from views/classes files to config][38]
* [Refactors try/except statements][39]
* [Test all try/except statements][40]
* [Export some APP & all ENV conf to .env][41]
* [Add a route for GET requests][43]
* [Use flask logger][44]
                                                    ]

[oc]: https://openclassrooms.com/fr/projects/creez-grandpy-bot-le-papy-robot "Créez GrandPy Bot, le papy-robot"
[approach]: https://gitlab.com/free_zed/grandpy/blob/master/doc/approach.md
[kanban]: https://github.com/freezed/ocp7/projects/1
[flask]: https://www.palletsprojects.com/p/flask/ "Flask is a Python web development _framework_ based on the Werkzeug, Jinja, MarkupSafe and itsdangerous pallets libraries."
[pytest]: https://pytest.org "Helps you write better programs"
[gmaps]: https://cloud.google.com/maps-platform/?hl=fr "API Google Maps"
[mediawiki]: https://www.mediawiki.org/wiki/API:Main_page/fr
[issues]: https://gitlab.com/free_zed/grandpy/issues
[05]: https://gitlab.com/free_zed/grandpy/issues/5
[23]: https://gitlab.com/free_zed/grandpy/issues/23
[26]: https://gitlab.com/free_zed/grandpy/issues/26
[36]: https://gitlab.com/free_zed/grandpy/issues/36
[38]: https://gitlab.com/free_zed/grandpy/issues/38
[39]: https://gitlab.com/free_zed/grandpy/issues/39
[40]: https://gitlab.com/free_zed/grandpy/issues/40
[41]: https://gitlab.com/free_zed/grandpy/issues/41
[43]: https://gitlab.com/free_zed/grandpy/issues/43
[44]: https://gitlab.com/free_zed/grandpy/issues/44
[heroku]: https://devcenter.heroku.com/articles/getting-started-with-python
[features]: https://gitlab.com/free_zed/grandpy/issues?utf8=%E2%9C%93&q=is%3Aissue+label%3Afunctionnality+
[log]: http://flask.pocoo.org/docs/1.0/logging/#logging
