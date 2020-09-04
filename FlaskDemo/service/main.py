# -*- coding: utf-8 -*-
import threading
from apscheduler.schedulers.blocking import BlockingScheduler
from FlaskDemo.db.db import DbClassNoPool
from FlaskDemo.service.settings import APS_SCHEDULER_CONFIG
from FlaskDemo.settings import PG_DB_URI
import logging

logging.basicConfig(level=logging.WARNING,
                    format='[Process %(process)d] [Thread %(thread)d] %(asctime)s %(filename)s '
                           '%(funcName)s[line:%(lineno)d] %(levelname)s '
                           '[message: %(message)s] ',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')

db = DbClassNoPool(PG_DB_URI)
Session = db.make_session()
scheduler = BlockingScheduler(APS_SCHEDULER_CONFIG)


class Service(threading.Thread):
    """定时任务mini版"""

    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop = False

    def run(self):
        if not scheduler.running:
            try:
                logging.warning("BlockingScheduler jobstore 启动！")
                scheduler.start()
            except (KeyboardInterrupt, SystemExit):
                logging.error("BlockingScheduler jobstore 退出！！")
                scheduler.shutdown()

    def stop(self):
        self.thread_stop = True


@scheduler.scheduled_job('cron', id='admin_test_task', minute='*/5', second='0')
def admin_task():
    """
    Admin模块  测试任务
    :return:
    """
    pg_session = Session()
    logging.warning("assessment_task start,time:")
    try:
        from FlaskDemo.admin.main_manager import ScheduleTask
        ScheduleTask.run(pg_session)
        logging.warning("assessment_task success!")
    except Exception as e:
        import traceback
        logging.error(traceback.format_exc())
        logging.warning("assessment_task error,msg:" + str(e))
    finally:
        if pg_session:
            pg_session.close()


if __name__ == "__main__":
    service = Service()
    service.start()
    service.join()
