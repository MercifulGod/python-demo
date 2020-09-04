# -*- coding: utf-8 -*-
from FlaskDemo.settings import PG_DB_URI
from sqlalchemy import create_engine

# ----------------------------- APS 调度配置 -----------------------------
# scheduler属性配置
APS_SCHEDULER_CONFIG = {
    'apscheduler.jobstores.default': {
        'type': 'memory'
    },
    'apscheduler.jobstores.sqlalchemy': {
        'type': 'sqlalchemy',
        'tablename': 'apscheduler_jobs',
        # 'url': PG_DB_URI,
        'engine': create_engine(PG_DB_URI, echo=False, encoding="utf-8", max_overflow=30, pool_size=10,
                                pool_recycle=3600)
    },
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '15'
    },
    'apscheduler.executors.processpool': {
        'type': 'processpool',
        'max_workers': '5'
    },
    'apscheduler.job_defaults.coalesce': 'true',
    'apscheduler.job_defaults.max_instances': '1',
    'apscheduler.job_defaults.misfire_grace_time': '3',
    'apscheduler.timezone': 'Asia/Shanghai',
}
# jobstore为数据库类型sqlalchemy的名称
JOBSTORE_SQLALCHEMY_NAME = "sqlalchemy"
