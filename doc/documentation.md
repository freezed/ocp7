Documentation
=============

## _Note_

_The latest updated version of this document is available at [github](https://github.com/freezed/ocp7/blob/master/documentation.md)._

_This is the full project's documentation, for a faster presentation, see the [presentation summary](https://github.com/freezed/ocp7/blob/master/doc/presentation.md) or [README.md](https://github.com/freezed/ocp7/blob/master/README.md)._

---

## Created with

- `python 3.6.6`
- `Flask 1.0.2`
- ~`Requests`~

## Runs

- on [Heroku][heroku]
    - `heroku CLI v7.9.4 linux-x64 node-v10.9.0`
- with `gunicorn 19.9.0`

## Installation

1. get the code : `git clone git@github.com:freezed/ocp7.git`
2. create a dedicated virtualenv : `python3 -m venv .venv`
3. store private API keys in environement variables locally in your `.venv` :
    - add `unset XXX_API_KEY` at bottom of `deactivate()` func° in  `.venv/bin/activate`
    - add `export XXX_API_KEY="xx-xx-nn-api_key"` at bottom of `.venv/bin/activate`
4. store your private API keys in environement variables locally in  heroku :
    - `heroku config:set XXX_API_KEY='xx-xx-nn-api_key'`
5. starts virtualenv  : `source .venv/bin/activate`
6. adds dependencies : `cd ocp7; pip install -r requirements.txt`

(…)

[heroku]: https://heroku.com
