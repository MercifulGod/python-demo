import asyncio
import uuid
import jwt
import json
import functools
import hashlib

from peewee import DoesNotExist
from datetime import datetime, date, time
from functools import partial
from bcrypt import hashpw, gensalt
from TornadoDemo.settings import settings
from apps.user.models import ZdUser


def auth_permission_required(perm=None):
    def decorator(view_func):
        @functools.wraps(view_func)
        async def _wrapped_view(self, *args, **kwargs):
            try:
                auth = self.request.headers.get('Authorization').split()
            except AttributeError:
                return await self.finish(
                    json.dumps({"code": 401, "message": "No authenticate header"}, default=json_serial))
            # 用户通过 API 获取数据验证流程
            if auth[0].lower() == "bearer":
                try:
                    payload = jwt.decode(auth[1], settings.get("cookie_secret"), algorithms=['HS256'])
                    mobile = payload.get('mobile')
                except jwt.ExpiredSignatureError:  # Token 过期
                    return await self.finish(json.dumps({"code": 401, "message": "Token expired"}, default=json_serial))
                except jwt.InvalidTokenError:  # 无效的Token值
                    return await self.finish(json.dumps({"code": 401, "message": "Invalid token"}, default=json_serial))
                except Exception as e:
                    return await self.finish(
                        json.dumps({"code": 401, "message": "Can not get user object"}, default=json_serial))
                try:
                    user = await self.application.objects.get(ZdUser, mobile=mobile)
                    if user.status == '0':
                        return await self.finish(json.dumps({"code": 401, "message": "该用户不可用"}, default=json_serial))
                    self._current_user = user
                except DoesNotExist as e:
                    return await self.finish(json.dumps({"code": 401, "message": "该用户不存在"}, default=json_serial))

                # Token 登录的用户判断是否有权限
                role_ids = SysUserRole.select(SysUserRole.role_id).where(SysUserRole.user_id == user.id)
                resource_ids = SysRoleResource.select(SysRoleResource.resource_id).where(
                    SysRoleResource.role_id.in_(role_ids))
                query = SysResource.select().where(SysResource.id.in_(resource_ids))
                resources = await self.application.objects.execute(query)
                permission_codes = [item.permission_code for item in resources]
                if perm is not None and len(set(perm).difference(set(permission_codes))) != 0:  # 用户没有通过权限验证
                    await self.finish(json.dumps({"code": 403, "message": "PermissionDenied"}, default=json_serial))

                # 此处很关键
                return await view_func(self, *args, **kwargs)
            else:
                await self.finish(json.dumps({"code": 401, "message": "Not support auth type"}, default=json_serial))

        return _wrapped_view

    return decorator


def json_serial(obj):
    if isinstance(obj, (datetime,)):
        return obj.isoformat().replace("T", " ")
    elif isinstance(obj, (date, time)):
        return obj.isoformat()
    elif isinstance(obj, (uuid.UUID,)):
        return str(obj)
    raise TypeError("Type {}s not serializable".format(type(obj)))


def hash_file(file_path=None, block_size=65536):
    hash_tool = hashlib.md5()
    file = open(file_path, 'rb')
    for buf in iter(partial(file.read, block_size), b''):
        hash_tool.update(buf)
    file.close()
    return hash_tool.hexdigest()


def encrypt_password(password=None):
    bcrypt_iterations = 12
    if isinstance(password, str):
        password = password.encode('utf-8')
    salt = gensalt(bcrypt_iterations)
    return password if password is None else hashpw(password, salt)


def check_password(password, db_password):
    password = password.encode('utf-8')
    return hashpw(password, db_password) == db_password
