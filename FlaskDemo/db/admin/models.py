# -*- coding: utf-8 -*-
import datetime
from FlaskDemo.db import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ARRAY, BigInteger

from FlaskDemo.admin.settings import USER_STATUS_RE


def now():
    return datetime.datetime.now


class User(Base):
    """
    文章
    """
    __tablename__ = 'user'

    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column('name', String(255), nullable=False, doc=u'用户名称')
    age = Column('age', Integer, nullable=False, doc=u'年龄')
    hobby = Column('hobby', ARRAY(Text), doc=u'爱好')
    desc = Column('desc', Text, nullable=False, doc=u'描述')
    status = Column('status', String(1), nullable=False, default=USER_STATUS_RE.get("启用"), doc=u'状态')
    create_time = Column("create_time", DateTime, nullable=False, default=now(), doc=u'创建时间')
    update_time = Column("update_time", DateTime, nullable=False, default=now(), onupdate=now(), doc=u'更新时间')
    role_id = Column('role_id', Integer, nullable=True, doc=u"角色id，关联角色表的id")


class MenuPerm(Base):
    """
    功能菜单权限分配资源表
    """
    __tablename__ = 'menu_perm'

    id = Column('id', BigInteger, primary_key=True, nullable=False, autoincrement=True)
    pid = Column('pid', BigInteger, nullable=True)
    name = Column('name', String(64), nullable=True)
    type = Column('type', String(64), nullable=True)
    status = Column('status', Integer, nullable=True, default=1)
    path = Column('path', String(255), nullable=True)

    def __init__(self, id=None, pid=None, name=None, status=None, path=None, type=None):
        self.id = id
        self.pid = pid
        self.name = name
        self.type = type
        self.status = status
        self.path = path


class Role(Base):
    """
    角色表
    """
    __tablename__ = 'role'

    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column('name', String(32), unique=True, nullable=False)
    menu_ids = Column('menu_ids', Text, nullable=True)
    create_time = Column('create_time', DateTime, default=now(), doc=u'创建时间')
    update_time = Column('update_time', DateTime, default=now(), onupdate=now(), doc=u'更新时间')
    user_id = Column('user_id', Integer, default=0, doc="用户ID")
    role_type = Column('role_type', Integer, default=0)
    role_category = Column('role_category', Integer, default=0)

    def __init__(self, id=None, name=None, create_time=None, menu_ids=None, update_time=None, user_id=0, role_type=0,
                 role_category=1):
        self.id = id
        self.name = name
        self.menu_ids = menu_ids
        self.create_time = create_time
        self.update_time = update_time
        self.user_id = user_id
        self.role_type = role_type
        self.role_category = role_category


class UserRolePerm(Base):
    """
    角色权限表（new）
    """
    __tablename__ = 'user_role_perm'

    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    role_id = Column('role_id', Integer)
    node_permission = Column('node_permission', String(1024), nullable=False)
    data_permission = Column('data_permission', String(1024))
    create_time = Column("create_time", DateTime, nullable=False, default=now(), doc=u'创建时间')
    update_time = Column("update_time", DateTime, nullable=False, default=now(), onupdate=now(), doc=u'更新时间')

    def __init__(self, id=None, role_id=None, node_permission=None, data_permission=None, create_time=None,
                 update_time=None, user_id=None):
        self.id = id
        self.role_id = role_id
        self.node_permission = node_permission
        self.data_permission = data_permission
        self.create_time = create_time
        self.update_time = update_time
        self.user_id = user_id
