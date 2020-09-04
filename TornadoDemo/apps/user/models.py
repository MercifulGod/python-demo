import uuid
from bcrypt import hashpw, gensalt
from datetime import datetime
from peewee import *
from TornadoDemo.settings import database


class PasswordHash(bytes):
    def check_password(self, password):
        password = password.encode('utf-8')
        return hashpw(password, self) == self


class PasswordField(BlobField):
    def __init__(self, iterations=12, *args, **kwargs):
        if None in (hashpw, gensalt):
            raise ValueError('Missing library required for PasswordField: bcrypt')
        self.bcrypt_iterations = iterations
        self.raw_password = None
        super(PasswordField, self).__init__(*args, **kwargs)

    def db_value(self, value):
        """Convert the python value for storage in the database."""
        if isinstance(value, PasswordHash):
            return bytes(value)

        if isinstance(value, str):
            value = value.encode('utf-8')
        salt = gensalt(self.bcrypt_iterations)
        return value if value is None else hashpw(value, salt)

    def python_value(self, value):
        """Convert the database value to a pythonic value."""
        if isinstance(value, str):
            value = value.encode('utf-8')

        return PasswordHash(value)


class ZdUser(Model):
    id = UUIDField(default=uuid.uuid4, primary_key=True, verbose_name=u"用户ID")
    name = CharField(max_length=20, null=True, verbose_name="昵称")
    mobile = CharField(max_length=11, verbose_name="手机号码", index=True, unique=True)
    password = PasswordField(verbose_name="密码")  # 1. 密文，2.不可反解
    is_superuser = BooleanField(default=False, verbose_name=u'是否管理员')
    photo = CharField(max_length=255, null=True, verbose_name='头像url地址')
    status = CharField(max_length=1, default='1', verbose_name=u'状态：0:禁用,1;启用')
    create_datetime = DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_datetime = DateTimeField(verbose_name="修改时间")
    last_login = DateTimeField(default=datetime.now, verbose_name="添加时间")
    is_effective = BooleanField(default=True, verbose_name=u'是否有效')

    class Meta:
        database = database
        db_table = 'zd_user'
