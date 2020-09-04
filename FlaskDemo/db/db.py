# -*- coding: utf-8 -*-

from FlaskDemo.db import Base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine
from FlaskDemo.settings import PG_DB_URI


class DbClass(object):
    def __init__(self, uri):
        self._engine = create_engine(uri, echo=False, encoding="utf-8", max_overflow=30, pool_size=10)
        self._metadata = Base.metadata

    def create_table(self):
        self._metadata.create_all(self._engine)

    def make_session(self):
        session_factory = sessionmaker(bind=self._engine)
        Session = scoped_session(session_factory)
        return Session


class DbClassNoPool(object):
    def __init__(self, uri=None):

        uri = PG_DB_URI if not uri else uri
        self._engine = create_engine(uri, echo=False, encoding="utf-8", poolclass=NullPool)
        self._metadata = Base.metadata

    def make_session(self):
        session_factory = sessionmaker(bind=self._engine)
        db_session = scoped_session(session_factory)
        return db_session
