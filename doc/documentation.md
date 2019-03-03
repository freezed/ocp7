Documentation
=============

## _Note_

_Latest version of this doc on [gitlab](https://gitlab.com/free_zed/grandpy/blob/master/documentation.md)._

---

## Created with

- `python 3.6.6`
- `Flask 1.0.2`
- `Requests`
- `pytest 3.7.3`

## Runs

- on [Heroku][heroku]
    - `heroku CLI v7.16.0 linux-x64 node-v10.10.0`
    - with `gunicorn 19.9.0`

## Installation

1. get the code : `git clone git@gitlab.com:free_zed/grandpy.git`
2. create a dedicated virtualenv : `python3 -m venv .venv`
3. store private API keys in environement variables locally in your `.venv` :
    - add `unset XXX_API_KEY` at bottom of `deactivate()` func° in  `.venv/bin/activate`
    - add `export XXX_API_KEY="xx-xx-nn-api_key"` at bottom of `.venv/bin/activate`
4. store your private API keys in environement variables locally in  heroku :
    - `heroku config:set XXX_API_KEY='xx-xx-nn-api_key'`
5. starts virtualenv  : `source .venv/bin/activate`
6. adds dependencies : `cd grandpy; pip install -r requirements.txt`
7. run tests : `pytest tests/test_classes.py`
8. run test coverage : `pytest --cov=flasklocal --cov-report html tests/test_*.py;`
9. run developement server : `python run.py`

[heroku]: https://heroku.com
