# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime
from FlaskDemo.db import Base


class Attachenment(Base):
    __tablename__ = "t_attachment"

    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    owner_type = Column('owner_type', String(64), nullable=False)
    file_name = Column('file_name', String(255), nullable=False)
    store_name = Column('store_name', String(64), nullable=False)
    preview_name = Column('preview_name', String(64), nullable=True)
    tag = Column('tag', String(255), nullable=True)
    create_time = Column('create_time', DateTime, nullable=True)
    user_id = Column('user_id', Integer, nullable=True)

    def __init__(self, id=None, owner_type=None, file_name=None, store_name=None, preview_name=None, tag=None,
                 create_time=None, user_id=None):
        self.id = id
        self.owner_type = owner_type
        self.file_name = file_name
        self.store_name = store_name
        self.preview_name = preview_name
        self.tag = tag
        self.create_time = create_time
        self.user_id = user_id
