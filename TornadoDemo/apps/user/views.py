import json
from peewee import DoesNotExist
from TornadoDemo.handler import BaseHandler, RedisHandler
from apps.common.utils import json_serial
from apps.user.models import ZdUser


class AddUser(RedisHandler):
    async def post(self, *args, **kwargs):
        form = json.loads(self.request.body.decode(encoding="utf-8")) if self.request.body else {}
        try:
            person, created = await self.application.objects.get_or_create(
                ZdUser, mobile=form.get("mobile"), defaults=form
            )
            if not created:
                return await self.finish(json.dumps({"code": "200", "msg": '该手机号以被使用'}, default=json_serial))
            await self.finish(json.dumps({"code": "200", "msg": '操作成功'}, default=json_serial))
        except Exception as e:
            await self.finish(json.dumps({"code": "500", "msg": '服务器异常'}, default=json_serial))


class UpdateUser(RedisHandler):
    async def post(self, *args, **kwargs):
        form = json.loads(self.request.body.decode(encoding="utf-8")) if self.request.body else {}
        try:
            user_count = await self.application.objects.count(ZdUser.select().where(ZdUser.id == form.get("id")))
            if user_count < 1:
                return await self.finish(json.dumps({"code": "500", "msg": '该用户不存在'}, default=json_serial))
            query = ZdUser.update(**form).where(ZdUser.id == form.pop("id"))
            update_count = await self.application.objects.execute(query)
            await self.finish(json.dumps({"code": "200", "msg": '操作成功'}, default=json_serial))
        except Exception as e:
            await self.finish(json.dumps({"code": "500", "msg": '服务器异常'}, default=json_serial))


class PasswordUpdate(RedisHandler):

    async def post(self, *args, **kwargs):
        form = json.loads(self.request.body.decode(encoding="utf-8")) if self.request.body else {}
        user_id = form.get('user_id')
        old_password = form.get('old_password')
        new_password = form.get('new_password')
        try:
            user = await self.application.objects.get(ZdUser, id=user_id)
        except DoesNotExist as e:
            return await self.finish(json.dumps({"code": "2001", "msg": '该用户不存在'}, default=json_serial))
        if not user.password.check_password(old_password):
            return await self.finish(json.dumps({"code": "2001", "msg": '该用户密码不正确'}, default=json_serial))
        user.password = new_password
        update_count = await self.application.objects.update(user)
        await self.finish(json.dumps({"code": "200", "msg": '操作成功'}, default=json_serial))


class ListUser(RedisHandler):
    async def post(self, *args, **kwargs):
        form = json.loads(self.request.body.decode(encoding="utf-8")) if self.request.body else {}
        offset = int(form.get('page_start', '0')) * int(form.get('page_size', '10'))
        limit = int(form.get('page_size', '10'))
        total_count = await self.application.objects.count(ZdUser.select())
        query = ZdUser.select().order_by(-ZdUser.create_datetime).limit(limit).offset(offset).dicts()
        users = await self.application.objects.execute(query)
        context = {
            "code": "200",
            "msg": '操作成功',
            "total_count": total_count,
            "data": []
        }
        for user in users:
            user.pop("password")
            user.pop("is_superuser")
            user.pop("is_effective")
            context.get('data').append(user)
        await self.finish(json.dumps(context, default=json_serial))


class DeleteUser(RedisHandler):
    async def post(self, *args, **kwargs):
        form = json.loads(self.request.body.decode(encoding="utf-8")) if self.request.body else {}
        query = ZdUser.delete().where(ZdUser.id.in_(form.get('user_id')))
        await self.application.objects.execute(query)
        await self.finish(json.dumps({"code": "200", "msg": '操作成功'}, default=json_serial))
#
