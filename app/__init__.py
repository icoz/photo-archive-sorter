#!/usr/bin/env python3
# coding: utf8

from flask import Flask
# from flask_login import LoginManager
# from flask_babel import Babel
# from flask_wtf.csrf import CSRFProtect
import logging
from logging.handlers import RotatingFileHandler
import config

__author__ = 'icoz'

app = Flask(__name__)
# print(config.PHAS_LOG)
app.config.from_object('config')
# for k in app.config:
#     print(f"{k}: {app.config[k]}")
# extended CSRF protection for JS
# csrf = CSRFProtect()
# csrf.init_app(app)

# add login support
# login_manager = LoginManager()
# login_manager.init_app(app)

# # L10n
# babel = Babel(app)

# add logging
formatter = logging.Formatter('''--------------------------------------------------
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s

Message:

%(message)s
''')
file_handler = RotatingFileHandler(app.config['PHAS_LOG'], maxBytes=1024 * 1024 * 10, backupCount=20)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

# from app import auth, db, views, forms
from app import db, views
