# -*- coding: utf-8 -*-
"""Base settings content"""
import fasteners

PROCESS_FILE_LOCK = fasteners.InterProcessLock('/tmp/tmp_lock_file')

UPLOAD_FILE_DIR = "/tmp/demo//upload"
UPLOAD_IMG_DIR = "/tmp/demo//static"
UPLOAD_UTIL = "/tmp/demo/util"
UPLOAD_FILE_ZIP_DIR = "/tmp/demo/zip"
DOWNLOAD_MESSAGE = u"文件正在生成中，请稍后刷新页面重试"

APP_CACHE = {'host': "127.0.0.1", 'port': 6379, 'db': 0, 'password': "123456"}
APP_SESSION = {'host': "127.0.0.1", 'port': 6379, 'db': 0, 'password': "123456"}

# CAS
CAS_SERVER = 'http://ip:port/cas/login'
CAS_LOGOUT = 'http://ip:port/cas/logout'
CAS_VALIDATE_ROUTE = '/cas/serviceValidate'

# 在线升级第三方账号信息
SECRET_KEY = 'dX6mg0jx0y`8(F_|wdgd3453453252345235433DB4f<J>7Q~*#{&F~'
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True

UPDATE_CACHE_KEY = "updating"
# postgres uri

PG_DB_URI = "postgresql://postgres:postgres@127.0.0.1:5432/demo"
MEMORY_LEAK_CHECK = False

SERVICE_THREADING = True

ALERT_ASSET_RELATION_FLAG = True

SQLALCHEMY_TRACK_MODIFICATIONS = True

# 邮件传输协议端口（ssl）
MAIL_TRANSFER_PROTOCOL_SSL_PORT = [465, 995, 993]

LOCALHOST_IP = '127.0.0.1'

# 短信类名
SMS_CLASS_NAME = 'SMS'
