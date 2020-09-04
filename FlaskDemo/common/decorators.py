# -*- coding: utf-8 -*-
"""Define decorators for views."""
import hashlib
import logging
import uuid
from datetime import datetime
from functools import wraps
from flask import g, session, request, jsonify, current_app

from FlaskDemo.admin.main_manager import LoginManage
from FlaskDemo.common.errors import ShowError


def login_required(f):
    """
    校验用户是否登录, login_token 会尝试从headers中或url参数中获取
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        login_token = request.headers.get('Authorization', '').split(' ')[-1]
        if not login_token:
            if request.headers.get('content-type') and request.headers.get('content-type') == 'application/json':
                params = request.json
            elif request.headers.get('content-type') and request.headers.get(
                    'content-type') == 'application/x-www-form-urlencoded':
                params = request.json
            else:
                params = request.form
            login_token = params.get('authorization', '') if params else ''
            if not login_token:
                csrf_token = session.get('csrf_token', '')
                username = session.get('username', None)
                if username:
                    return f(*args, **kwargs)
                return jsonify({'code': 303, 'status': 0, 'message': u'请登录系统', 'data': [], 'token': csrf_token})
        token_key = 'app_token_' + login_token
        user = current_app.cache.get(token_key, format="json")
        if not user:
            return jsonify({'code': 303, 'status': 0, 'message': u'请登录系统', 'data': [], 'token': ''})
        session['username'] = user.get('username')
        session['uid'] = user.get('uid') if (user.get("uid") and user.get("uid") != "") else None
        return f(*args, **kwargs)

    return decorated_function


def permission_required(app_ids):
    """
    登录用户权限校验
    :param app_id:
    :return:
    """

    def decorated_function(f):
        @wraps(f)
        def __decorated_function(*args, **kwargs):
            token = session.get('csrf_token', '')
            username = session.get('username', None)
            uid = session.get('uid', None)
            if app_ids is None:
                return jsonify({'code': 403, 'status': 0, 'message': u'当前用户没有该APP权限', 'data': [], 'token': token})
            app_ids_list = app_ids.split(',')
            if not username or not uid:
                return jsonify({'code': 303, 'status': 0, 'data': [], 'message': u'登录超时，请重新登录', 'token': token})
            result_info = LoginManage.get_login_user_app_menus(uid)
            if result_info['status'] != 1:
                return jsonify({'code': 500, 'status': 0, 'data': [], 'message': u'服务器异常', 'token': token})
            if not set(app_ids_list) & set(result_info["data"]):
                return jsonify({'code': 302, 'status': 0, 'data': [], 'message': u'当前用户没有该APP权限', 'token': token})
            return f(*args, **kwargs)

        return __decorated_function

    return decorated_function


def exception_catch(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get('csrf_token', '')
        try:
            return f(*args, **kwargs)
        except ShowError as e:
            return jsonify({'status': 500, 'message': e.message, 'token': token})
        except Exception as e:
            logging.error('catch exception: %s, function name : %s ' % (str(e), f.__name__), exc_info=1)
            return jsonify({'status': 500, 'message': u'服务器内部错误', 'token': token})

    return decorated_function


def token_uuid():
    uid = str(uuid.uuid1())
    uname = session.get('username', '')
    return hashlib.md5(uid + uname).hexdigest()


def reset_csrf_token():
    tmp_token = token_uuid()
    session['csrf_token'] = tmp_token
    session['csrf_timeout'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return tmp_token


def get_crsf_token(request):
    header_token = request.headers.get('csrf_token', None)
    url_token = request.args.get("csrf_token")
    try:
        json_token = request.json.get('csrf_token')
    except Exception as e:
        json_token = None
    try:
        form_token = request.form.get('csrf_token')
    except Exception as e:
        form_token = None
    csrf_token = header_token or url_token or json_token or form_token
    return csrf_token


def csrf_protect(f, template=None):
    """
    处理频繁请求操作或跨站请求
    :param f:
    :param template: 4.3模板路径
    :return:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "POST":
            content_type = request.headers.get("content-type")
            # 导入文件接口，不做校验
            if content_type == "multipart/form-data":
                return f(*args, **kwargs)
            token = session.pop('csrf_token', '')
            stime = session.get('csrf_timeout')
            start = datetime.strptime(stime, '%Y-%m-%d %H:%M:%S') if stime else datetime.now()
            now = datetime.now()
            delta = abs(now - start)
            _token = get_crsf_token(request)

            # 如果传入token或者session中的token为空，重新生成并返回
            if not _token or _token != token:
                return jsonify({'code': 403, 'status': 0, 'message': u'csrf_token有误，请重试！', "token": reset_csrf_token()})
            # 如果30秒之内，不判断token是否相等(考虑并发问题)
            if delta.seconds <= 30:
                return f(*args, **kwargs)
            elif delta.seconds < 3600:
                return jsonify({'code': 403, 'status': 0, 'message': u'csrf_token超时，请重试！', "token": reset_csrf_token()})
            return f(*args, **kwargs)
        return f(*args, **kwargs)

    return decorated_function


def generate_csrf_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'csrf_token' not in session:
            session['csrf_token'] = token_uuid()
        session['csrf_timeout'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f(*args, **kwargs)

    return decorated_function


if __name__ == "__main__":
    pass
