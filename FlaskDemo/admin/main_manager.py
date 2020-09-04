# -*- coding: utf-8 -*-

import copy
import hashlib
import uuid

from sqlalchemy import cast, String
from datetime import datetime

from flask import session, g, current_app
from FlaskDemo.admin.service import MenuService, RolePermService, UserService
from FlaskDemo.admin.settings import USER_STATUS, MENU_TYPE_RE, PASSWORD_ROLE
from FlaskDemo.common.errors import ShowError
from FlaskDemo.common.helper.service import CommonService
from FlaskDemo.db.admin.models import User, AppMenuPerm, UserRolePerm, Role


class UserMain(object):
    """
    用户管理类
    """

    @staticmethod
    def user_insert_or_update(form=None):
        params = copy.deepcopy(form)
        if form.get("id"):
            f = [User.id == form.get("id")]
            CommonService.update_by_attrs(User, f, form)
        else:
            params.setdefault("create_user", session.get('username', "管理员"))
            CommonService.add_record(User, params)

    @staticmethod
    def user_del(form=None):
        if not form.get("ids"):
            raise ShowError("请选择要删除的用户")
        filters = [User.id.in_(form.get("ids"))]
        CommonService.update_by_attrs(User, filters, {"status": USER_STATUS.get("删除")})

    @staticmethod
    def user_list(form=None):
        filters = []
        if form.get("status"):
            filters.append(User.status == form.get("status"))
        if form.get("keyword"):
            filters.append(
                User.name.like("%{name}%".format(name=form.get("keyword"))) |
                User.desc.like("%{desc}%".format(desc=form.get("keyword")))
            )
        ret = CommonService.list_by_filter(User, filters, form)
        return ret

    @staticmethod
    def user_detail(form=None):
        user = CommonService.get_by_id(User, form.get("id"))
        return user.to_dict()

    @staticmethod
    def get_by_name(form=None):
        user = UserService.get_by_name(form.get("name"))
        return user


class MenuMain(object):

    @staticmethod
    def check_app_id(form):
        """检查APP_ID是否存在"""
        app = CommonService.get_by_id(AppMenuPerm, form.get("app_id"))
        ret = 1 if app else 0
        return ret

    @staticmethod
    def insert_or_update(form):
        menu = CommonService.get_by_id(AppMenuPerm, form.get("id"))
        if menu:  # 更新菜单
            CommonService.update_by_obj(menu, form)
            return
        menu = CommonService.add_record(AppMenuPerm, form)

        # 默认为系统管理员角色添加菜单权限
        user_role_perm = UserRolePerm()
        user_role_perm.role_id = 1  # 系统管理员角色
        user_role_perm.node_permission = form.get("id")
        user_role_perm.create_time = datetime.now()
        user_role_perm.update_time = datetime.now()
        role = CommonService.save_by_obj(user_role_perm)

    @staticmethod
    def app_menu_del(form):
        result_info = dict()
        app_menu = MenuService.list_menu([AppMenuPerm.pid == form.get("app_id")])
        if app_menu:
            raise ShowError("存在子节点，请先删除字节点！")
        MenuService.del_menu(form.get("app_id"))
        return result_info

    @staticmethod
    def app_menu_list(form):
        ret = []
        f = [AppMenuPerm.type == MENU_TYPE_RE.get("一级菜单")]
        ids = g.pg_db.query(AppMenuPerm.id).filter(*f).order_by(AppMenuPerm.id).all()
        for app_id in ids:
            ret.extend(MenuMain.get_all_child(app_id[0]))
        return ret

    @staticmethod
    def get_all_child(app_id):
        ret = MenuService.list_menu([cast(AppMenuPerm.id, String).like(str(app_id) + "%")])
        return ret


class RoleManage(object):

    @staticmethod
    def insert_or_update(form):
        if form.get("name").strip() == '':
            raise ShowError("角色名不能为空")
        if form.get("id"):
            f = [Role.name == form.get("name"), Role.id != form.get("id")]
        else:
            f = [Role.name == form.get("name")]
        roles = CommonService.list_select_by_filter([Role.id], f)
        if roles:
            raise ShowError("该角色已存在")
        db_session = g.pg_db
        try:
            # 创建角色
            role = Role()
            for key, value in form.items():
                if key is not None:
                    setattr(role, key, value)
            role = db_session.merge(role)

            # 创建角色对应的权限
            db_session.query(UserRolePerm).filter(UserRolePerm.role_id == role.id).delete(synchronize_session=False)

            node_permission_list = form.get("node_permission").split(',')
            node_permission_list = [{"role_id": role.id, "node_permission": item} for item in node_permission_list]
            db_session.bulk_insert_mappings(UserRolePerm, node_permission_list)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise ShowError("添加角色失败")

    @staticmethod
    def get_role_by_id(form):
        """
        跟据id获取角色
        :return:
        """
        role = CommonService.get_by_id(Role, form.get("id"))
        return role

    @staticmethod
    def delete_roles(form):
        """
        角色批量删除
        :return:
        """
        CommonService.del_by_ids(Role, [form.get("role_ids")])

    @staticmethod
    def get_all_roles(form):
        roles = CommonService.list_by_filter(Role, filters=[], params=form)
        return roles


class LoginManage(object):

    @staticmethod
    def token_uuid():
        user_id = str(uuid.uuid1())
        user_name = session.get('username', '')
        return hashlib.md5(user_id + user_name).hexdigest()

    @staticmethod
    def check_login_fail_time(username):
        """
        校验缓存重存放的连续多次登录失败用户
        :return:
        """
        result_info = {'status': 1, 'message': u'验证通过'}
        if username == 'admin':
            return result_info
        # 获取缓存中登录失败的用户（多次登录失败）
        login_fail_user = current_app.cache.get('login_fail_user', format='json')
        password_role = PASSWORD_ROLE
        fail_count = password_role["failure_logon"]
        if login_fail_user and username in login_fail_user:
            login_user = login_fail_user[username]
            last_login_time = datetime.strptime(login_user["last_login_time"], '%Y-%m-%d %H:%M-%S')
            last = datetime.now() - last_login_time
            if last.seconds < 300 and login_user["count"] >= fail_count != 0:
                message = u'该账号已被锁定，请' + str(5 - last.seconds / 60) + u'分钟以后重试！'
                result_info = {'status': 0, 'message': message}
            elif last.seconds >= 300:
                login_fail_user.pop(username, None)
                current_app.cache.set('login_fail_user', login_fail_user, format='json', ex=24 * 60 * 60)
        return result_info

    @staticmethod
    def check_password_expired(username):
        """
        校验密码是否已经过期，以及处理方式
        :param username:
        :return:
        """
        if username == 'admin':
            result_info = {'status': 1, 'message': u'验证通过', }
            return result_info
        else:
            try:
                user = g.pg_db.query(User).filter(User.name == username).first()
                password_role = PASSWORD_ROLE
                if user.pwd_time == '':
                    result_info = {'status': 0, 'message': u'用户初始密码时间为空'}
                    return result_info
                if password_role["valid_day"] == 0:
                    result_info = {'status': 1, 'message': u'验证通过', }
                    return result_info

                now_time = datetime.now()
                start_time = user.pwd_time
                # 密码天数
                pwd_day = (now_time - start_time).days + 1
                # 密码有效天数
                vllid_day = password_role["valid_day"]
                # 密码修改提醒
                warn_day = password_role["warn_day"]
                # 密码剩余天数
                last_day = vllid_day - pwd_day
                if pwd_day > vllid_day:
                    if password_role["handle"] == 1:
                        result_info = {'status': 2, 'message': u'建议用户登录后重置密码', 'last_day': last_day}
                        return result_info
                    else:
                        g.pg_db.query(User).filter(User.name == username).update({"status": 0},
                                                                                 synchronize_session=False)
                        g.pg_db.commit()
                        result_info = {'status': 0, 'message': u'用户密码过期，账户被锁定', }
                        return result_info
                else:
                    if last_day > warn_day:
                        result_info = {'status': 1, 'message': u'验证通过', }
                        return result_info
                    else:
                        result_info = {'status': 2, 'message': u'建议用户登录后重置密码', 'last_day': last_day}
                        return result_info
            except Exception as e:
                g.pg_db.rollback()
                result_info = {'status': 0, 'message': u'服务器调用异常', }
                return result_info

    @staticmethod
    def get_login_user_app_menus(user_id):
        """
        获取登录用户节点权限信息(list)
        :param uid:
        :return:
        """
        user_app_menus = set()
        user = CommonService.get_by_id(User, user_id)
        list_role_perms = RolePermService.list_perm([UserRolePerm.role_id == user.role_id])
        for role_perm in list_role_perms:
            user_app_menus.add(role_perm.node_permission)
        return list_role_perms


class ScheduleTask(object):
    @staticmethod
    def run(pg_session):
        pass
