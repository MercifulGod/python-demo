from peewee import *
from datetime import datetime
from TornadoDemo.TornadoDemo.settings import database


class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        database = database
