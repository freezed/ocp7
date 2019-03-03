#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: [freezed](https://gitlab.com/free_zed) 2018-08-23
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

This file is part of project [grandpy](https://gitlab.com/free_zed/grandpy/).
"""
from flasklocal import app

if __name__ == '__main__':
    app.run(
        app.config['HOST'],
        app.config['PORT'],
        app.config['APP']['DEBUG'],
    )
