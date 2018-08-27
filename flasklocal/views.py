#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: freezed <freezed@users.noreply.github.com> 2018-08-21
Version: 0.1
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

This file is part of [ocp7](http://github.com/freezed/ocp7/) project.

"""
import pprint
from flask import Flask, request, render_template
from apicall import goo_geocode, goo_static

app = Flask(__name__)
app.config.from_object('config')


@app.route('/', methods=['POST', 'GET'])
def index():
    """ Index View """

    # Catch posted data from form
    if "submit" in request.form:
        address = str(request.form['query'])
        api_response = pprint.pformat(goo_geocode(address))

    else:
        # Default response
        api_response = "… empty response …"

    # Redern view with vars
    return render_template(
        "index.html",
        name=app.config['APP']['NAME'],
        url=app.config['APP']['SRC'],
        raw_response=api_response,
        map_url=goo_static(),
    )


if __name__ == "__main__":
    app.run()
