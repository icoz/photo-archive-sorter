#!/usr/bin/env python3
# coding: utf8

import sys
import os

DEBUG = True
ENV = "devel"

# database settings
DATABASE_URI = "mongodb://localhost:27017"
DATABASE_NAME = "phas_test"

# datetime format for search form
DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'

# log file
# if sys.platform == 'win32':
#     basedir = os.path.abspath(os.path.dirname(__file__))
#     PhAS_LOG = os.path.join(basedir, 'python.log')
# else:
PHAS_LOG = os.environ.get('PhAS_LOG') or './phas.log' or '/var/log/PhAS_LOG/python.log'


