# coding:utf-8

import os
import peewee_async
from peewee_async import Manager

BASE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(os.path.join(BASE_ROOT, "static"), "media")
static_root = os.path.join(BASE_ROOT, "static")
MEDIA_URL = "/static/media"

# Application配置参数
settings = dict(
    template_path=os.path.join(BASE_ROOT, "templates"),
    static_path=os.path.join(BASE_ROOT, "static"),
    cookie_secret="FhLXI+BRRomtuaGRRomtuaG47hoRRomtuaG47hoI=",
    xsrf_cookies=False,
    login_url='/login',
    debug=True
)

# Redis配置参数
redis_options = dict(
    host="192.168.1.252",
    port=6379,
    password="123456"
)

# 密码加密密钥
passwd_hash_key = "BRRomtuaGRRomtuaG47hoRRomtuaG47hoI+BBx2WQ="

# MySQL数据库
database = peewee_async.MySQLDatabase(
    'demo', host="127.0.0.1", port=3306, user="root", password="123456"
)
async_database = Manager(database)

# 日志配置
log_path = os.path.join(os.path.dirname(__file__), "logs/log")
log_level = "debug"
