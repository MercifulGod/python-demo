# -*- coding: utf-8 -*-
from flask import g
from sqlalchemy import func, desc, and_, asc, or_, extract, distinct

from FlaskDemo.db.admin.models import User, MenuPerm, UserRolePerm


class UserService(object):
    """
    用户服务类
    """

    @staticmethod
    def count_user(filter_param=None):
        """ 用户计数
        :return:
        """
        db_session = g.pg_db
        ret = db_session.query(func.count(User.id)).filter(*filter_param).scalar()
        return ret

    @staticmethod
    def get_by_name(name):
        db_session = g.pg_db
        ret = db_session.query(User).filter(User.name == name).first()
        return ret


class MenuService(object):
    """
    用户服务类
    """

    @staticmethod
    def list_menu(filter_param=None):
        """ 用户计数
        :return:
        """
        db_session = g.pg_db
        ret = db_session.query(MenuPerm).filter(*filter_param).order_by(MenuPerm.id).all()
        return [item.to_dict() for item in ret]

    @staticmethod
    def del_menu(_id):
        """
        修改角色
        """
        filter_param = MenuPerm.id == _id
        filter_param_role = [UserRolePerm.node_permission == str(_id), UserRolePerm.role_id == 1]
        try:
            g.pg_db.query(MenuPerm).filter(filter_param).delete(synchronize_session=False)
            g.pg_db.query(UserRolePerm).filter(*filter_param_role).delete(synchronize_session=False)
            g.pg_db.commit()
        except Exception as e:
            g.pg_db.rollback()
            raise e


class RolePermService(object):
    """
    用户服务类
    """

    @staticmethod
    def list_perm(filter_param=None):
        """ 用户计数
        :return:
        """
        db_session = g.pg_db
        ret = db_session.query(UserRolePerm).filter(*filter_param).all()
        return ret

    @staticmethod
    def del_menu(_id):
        """
        修改角色
        """
        filter_param = MenuPerm.id == _id
        filter_param_role = [UserRolePerm.node_permission == str(_id), UserRolePerm.role_id == 1]
        try:
            g.pg_db.query(MenuPerm).filter(filter_param).delete(synchronize_session=False)
            g.pg_db.query(UserRolePerm).filter(*filter_param_role).delete(synchronize_session=False)
            g.pg_db.commit()
        except Exception as e:
            g.pg_db.rollback()
            raise e
