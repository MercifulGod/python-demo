# -*- coding: utf-8 -*-
"""create flask app."""

import logging
import traceback

from flask import Flask, g

from FlaskDemo import settings
from FlaskDemo.db.db import DbClass
# from FlaskDemo.common.session import MSession
from FlaskDemo.settings import PROCESS_FILE_LOCK, APP_CACHE, APP_SESSION
from FlaskDemo.common.cache import Cache
from FlaskDemo.common.register import Register
from flask_cas import CAS

#
# class WingsAppHolder(object):
#     def __init__(self, app, db):
#         """init before request"""
#         self.app = app
#         self.db = db
#         self.app.before_request(self.before_request)
#         self.app.teardown_request(WingsAppHolder.teardown_request)
#
#     def before_request(self):
#         """handle before request"""
#         session = self.db.make_session()
#         g.pg_db = session()
#
#     @staticmethod
#     def teardown_request(exception):
#         """handle after request"""
#
#         db_session = g.get("pg_db")
#         if db_session:
#             db_session.close()
#         if exception is not None:
#             logging.error(traceback.format_exc())


def _bind_database(app, db):
    """bind database"""

    def before_request():
        """handle before request"""
        session = db.make_session()
        g.pg_db = session()

    def teardown_request(exception):
        """handle after request"""
        db_session = g.get("pg_db")
        if db_session:
            db_session.close()
        if exception is not None:
            logging.error(traceback.format_exc())

    app.before_request(before_request)
    app.teardown_request(teardown_request)


def _init_database(db):
    """init database and init the edition info about situation"""
    db.create_table()


def init_app():
    """ 初始化APP
    :return:
    """
    app = CAS(Flask(__name__)).app
    app.config.from_object(settings)
    # initialize database
    logging.basicConfig(level=logging.DEBUG)
    return app


def create_app(settings=None, name=None):
    """
    init_app config & global setting , redis etc;
    :param settings:
    :param name:
    :return:
    """
    app = init_app()
    app.cache = Cache(**APP_CACHE)
    app.session = Cache(**APP_SESSION)
    # app.session_interface = MSession()
    Register(app)

    db = DbClass(app.config.get("PG_DB_URI"))
    with PROCESS_FILE_LOCK:
        _init_database(db)
    _bind_database(app, db)
    return app
