#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: [freezed](https://gitlab.com/free_zed) 2018-08-21
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

This file is part of project [grandpy](https://gitlab.com/free_zed/grandpy/).
"""
from flask import Flask, request, render_template, jsonify
from pprint import pformat as pf
from .classes import Place, Query, Message

app = Flask(__name__)
app.config.from_object('config')

@app.route('/ask', methods=['POST'])
def ask():
    """ Route to provide connection with JS frontend """
    # Catch posted data from form
    if "textinput" in request.form:
        # Parse text input
        query = Query(request.form['textinput'])
        query.parse()

        # Request & filter data
        place = Place(query.in_string)

        # basic server loggin
        log = [
            "input :[{}]".format(request.form['textinput']),
            "string:[{}]".format(query.in_string),
        ]
        place.trigger_api()
        log.append("query :[{}]".format(place.query))

        msg = Message(place)
        view_vars = {'question': request.form['textinput']}

        # Get map URL for address
        if place.geo_data['status']:
            view_vars.update(msg.address_yes())

        else:
            # No geo_data : feeds with place.geo_data for loggin
            view_vars.update(msg.address_no())
            log.append("geo_data=#\n{}#".format(pf(place.geo_data)))

        # Get wikimedia data
        if place.article_data['status']:
            view_vars.update(msg.extract_yes())

        else:
            # No extract : feeds with place.article_data for loggin
            view_vars.update(msg.extract_no())
            log.append("article_data=#\n{}#".format(pf(place.article_data)))

        # print server loggin
        for line in log:
            print(line)

    return jsonify(view_vars)


@app.route('/')
def index():
    """ Landing page """
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
