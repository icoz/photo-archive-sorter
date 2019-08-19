#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config 
from app import app
from os import environ as env

__author__ = 'icoz'

# if env.get('PhAS_PRODUCTION'):
#     app.run(host='0.0.0.0', port=80)
# else:
app.run(debug=True, host='0.0.0.0', port=5000)
