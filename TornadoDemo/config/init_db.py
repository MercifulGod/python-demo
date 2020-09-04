from peewee import MySQLDatabase
from TornadoDemo.apps.user.models import ZdUser

database = MySQLDatabase('demo', host="127.0.0.1", port=3306, user="root", password="123456")


def init():
    # 生成表
    database.create_tables([ZdUser])


if __name__ == "__main__":
    init()
