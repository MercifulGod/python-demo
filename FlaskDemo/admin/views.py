# coding=utf-8

import logging
import traceback
from flask import (session, jsonify, request, Blueprint, g)
from FlaskDemo.common.errors import ShowError
from FlaskDemo.admin.main_manager import UserMain, MenuMain, RoleManage, LoginManage
from FlaskDemoBak.db.admin.models import User
from FlaskDemo.common.decorators import csrf_protect, generate_csrf_token, exception_catch, \
    login_required, permission_required

NAMESPACE = 'admin'
admin = Blueprint(NAMESPACE, __name__)


@admin.route('/login', methods=['GET', 'POST'])
def login():
    """
    用户登录逻辑
    post： 登录操作
    get:   验证用户是否登录
    :return:
    """
    data = dict()
    if request.method == 'POST':
        try:
            param = request.json
            username = param.get('username', '')
            password_encrypt = param.get('password', '')
            user = g.pg_db.query(User).filter(User.name == username).first()

            check_time_info = LoginManage.check_login_fail_time(username)
            if check_time_info.get('status') == 0:
                return jsonify({'code': 204, 'status': check_time_info['status'], 'data': [''],
                                'message': check_time_info['message'], 'token': ''})

            # 验证用户名，密码是否正确，并做相关业务处理

            # 校验用户密码是否过期
            message = '登录成功'
            check_password_expired = LoginManage.check_password_expired(username)
            if check_password_expired.get('status') == 0:
                return jsonify({'code': 205, 'status': check_password_expired['status'], 'data': [''],
                                'message': check_password_expired['message'], 'token': ''})

            csrf_token = LoginManage.token_uuid()
            session['csrf_token'] = csrf_token
            session['uid'] = user.id
            session['username'] = username
        except Exception as e:
            logging.warn('[%s] Login Error: %s', NAMESPACE, e, exc_info=1)
            return jsonify({'code': 500, 'status': 0, 'data': data, 'message': '服务器异常', 'token': ''})
        return jsonify({'code': 200, 'status': 1, 'data': data,
                        'message': message, 'token': csrf_token})
    else:
        username = session.get('username', None)
        uid = session.get('uid', None)
        csrf_token = session.get('csrf_token', '')
        if username and uid:
            data['username'] = username
            return jsonify({'code': 200, 'status': 1, 'data': data, 'message': '登录成功', 'token': csrf_token})
        else:
            return jsonify({'code': 303, 'status': 0, 'data': [], 'message': '请重新登录', 'token': csrf_token})


@admin.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    退出登录，清空session
    :return:
    """
    session.clear()
    return jsonify({'code': 200, 'status': 1, 'data': [], 'message': 'logout success', 'token': ''})


@admin.route('/user_insert_or_update', methods=("GET", "POST"))
@login_required
@csrf_protect
@generate_csrf_token
@permission_required('19,11')
@exception_catch
def user_insert_or_update():
    token = session.get('csrf_token', '')
    form = request.get_json() if request.method == "POST" else request.args
    try:
        UserMain.user_insert_or_update(form)
        return jsonify(code=200, status=1, message=u"成功", data={}, token=token)
    except Exception as e:
        logging.error(traceback.format_exc())
        msg = str(e) if e.__class__ == ShowError else u"新增或删除用户失败"
        return jsonify(code=500, status=0, message=msg, data={}, token=token)


@admin.route('/service/user_del', methods=("GET", "POST"))
@login_required
@csrf_protect
@generate_csrf_token
@permission_required('19,11')
@exception_catch
def user_del():
    token = session.get('csrf_token', '')
    form = request.get_json() if request.method == "POST" else request.args
    try:
        UserMain.user_del(form)
        return jsonify(code=200, status=1, message=u"成功", data={}, token=token)
    except Exception as e:
        logging.error(traceback.format_exc())
        msg = str(e) if e.__class__ == ShowError else u"删除用户失败"
        return jsonify(code=500, status=0, message=msg, data={}, token=token)


@admin.route('/service/user_list', methods=("GET", "POST"))
@login_required
@csrf_protect
@generate_csrf_token
@permission_required('19,11')
@exception_catch
def user_list():
    token = session.get('csrf_token', '')
    form = request.get_json() if request.method == "POST" else request.args
    try:
        ret = UserMain.user_list(form)
        return jsonify(code=200, status=1, message=u"成功", data=ret, token=token)
    except Exception as e:
        logging.error(traceback.format_exc())
        msg = str(e) if e.__class__ == ShowError else u"获取用户列表失败"
        return jsonify(code=500, status=0, message=msg, data={}, token=token)


@admin.route('/service/user_detail', methods=("GET", "POST"))
@login_required
@csrf_protect
@generate_csrf_token
@permission_required('19,11')
@exception_catch
def user_detail():
    token = session.get('csrf_token', '')
    form = request.get_json() if request.method == "POST" else request.args
    try:
        ret = UserMain.user_detail(form)
        return jsonify(code=200, status=1, message=u"成功", data=ret, token=token)
    except Exception as e:
        logging.error(traceback.format_exc())
        msg = str(e) if e.__class__ == ShowError else u"获取用户详情失败"
        return jsonify(code=500, status=0, message=msg, data={}, token=token)


@admin.route('/service/check_app_id', methods=["GET"])
def check_app_id():
    token = session.get('csrf_token', '')
    form = request.get_json() if request.method == "POST" else request.args
    try:
        ret = MenuMain.check_app_id(form)
        return jsonify(code=200, status=1, message=u"成功", data=ret, token=token)
    except Exception as e:
        logging.error(traceback.format_exc())
        msg = str(e) if e.__class__ == ShowError else u"获取用户详情失败"
        return jsonify(code=500, status=0, message=msg, data={}, token=token)


@admin.route('/service/menu_insert_or_update', methods=["POST"])
def menu_insert_or_update():
    """
    获取 app info
    is_update 0-add 1-update
    """
    token = session.get('csrf_token', '')
    form = request.get_json() if request.method == "POST" else request.args
    try:
        ret = MenuMain.insert_or_update(form)
        return jsonify(code=200, status=1, message=u"成功", data=ret, token=token)
    except Exception as e:
        logging.error(traceback.format_exc())
        msg = str(e) if e.__class__ == ShowError else u"获取用户详情失败"
        return jsonify(code=500, status=0, message=msg, data={}, token=token)


@admin.route('/service/menu_del', methods=["POST", "GET"])
def menu_del():
    """
    获取 app info
    is_update 0-add 1-update
    """
    token = session.get('csrf_token', '')
    form = request.get_json() if request.method == "POST" else request.args
    try:
        ret = MenuMain.app_menu_del(form)
        return jsonify(code=200, status=1, message=u"成功", data=ret, token=token)
    except Exception as e:
        logging.error(traceback.format_exc())
        msg = str(e) if e.__class__ == ShowError else u"获取用户详情失败"
        return jsonify(code=500, status=0, message=msg, data={}, token=token)


@admin.route('/service/menu_list', methods=["GET"])
def menu_list():
    """
    获取 app info
    """
    token = session.get('csrf_token', '')
    form = request.get_json() if request.method == "POST" else request.args
    try:
        ret = MenuMain.app_menu_list(form)
        return jsonify(code=200, status=1, message=u"成功", data=ret, token=token)
    except Exception as e:
        logging.error(traceback.format_exc())
        msg = str(e) if e.__class__ == ShowError else u"获取菜单列表"
        return jsonify(code=500, status=0, message=msg, data={}, token=token)


# =========================role配置======================================================
@admin.route('/service/role_insert_or_update', methods=['POST'])
@login_required
@csrf_protect
@generate_csrf_token
@permission_required('19,11')
@exception_catch
def role_insert_or_update():
    """
    保存角色：角色表 ，角色权限表
    :return:
    """
    token = session.get('csrf_token', '')
    form = request.get_json() if request.method == "POST" else request.args
    try:
        ret = RoleManage.insert_or_update(form)
        return jsonify(code=200, status=1, message=u"成功", data=ret, token=token)
    except Exception as e:
        logging.error(traceback.format_exc())
        msg = str(e) if e.__class__ == ShowError else u"获取菜单列表"
        return jsonify(code=500, status=0, message=msg, data={}, token=token)


@admin.route('/role/getRoleList', methods=['GET', 'POST'])
@login_required
@csrf_protect
@generate_csrf_token
@permission_required('19,11')
@exception_catch
def get_role_list():
    """
    角色查询，加载，分页
    :return:
    """
    token = session.get('csrf_token', '')
    form = request.get_json() if request.method == "POST" else request.args
    try:
        ret = RoleManage.get_all_roles(form)
        return jsonify(code=200, status=1, message=u"成功", data=ret, token=token)
    except Exception as e:
        logging.error(traceback.format_exc())
        msg = str(e) if e.__class__ == ShowError else u"获取菜单列表"
        return jsonify(code=500, status=0, message=msg, data={}, token=token)


@admin.route('/role/deleteRoleList', methods=['POST', 'GET'])
@login_required
@csrf_protect
@generate_csrf_token
@permission_required('19,11')
@exception_catch
def delete_roles():
    """
    角色批量删除
    :return:
    """
    token = session.get('csrf_token', '')
    form = request.get_json() if request.method == "POST" else request.args
    try:
        ret = RoleManage.delete_roles(form)
        return jsonify(code=200, status=1, message=u"成功", data=ret, token=token)
    except Exception as e:
        logging.error(traceback.format_exc())
        msg = str(e) if e.__class__ == ShowError else u"删除角色失败"
        return jsonify(code=500, status=0, message=msg, data={}, token=token)

# =========================role end======================================================
