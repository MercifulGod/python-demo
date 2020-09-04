# coding = utf-8

import time
import functools
import logging
import signal
import tornado.ioloop
import tornado.netutil
import tornado.process
from tornado import web
from tornado.httpserver import HTTPServer
from tornado.options import options, define
from peewee_async import Manager

from apps.user.tasks import user_task
from TornadoDemo.urls import urlpatterns
from TornadoDemo.settings import settings, database

# create logger
logger = logging.getLogger('root')
define("port", default=5000, type=int, help="run server on the given port")


class Application(tornado.web.Application):
    def __init__(self):
        self.objects = Manager(database)
        database.set_allow_sync(False)  # No need for sync anymore!
        super(Application, self).__init__(urlpatterns, **settings)


def task_initialize():
    """功能：定义定时任务，并启动定时任务
    :return : 返回任务列表，用于停止任务
    """
    task_list = []

    task = functools.partial(user_task, name="张三")
    periodic_task = tornado.ioloop.PeriodicCallback(task, 1000 * 30)  # 30秒更新一次wifi设备和用户表
    task_list.append(periodic_task)

    for task in task_list:
        task.start()
    return task_list


def server_initialize():
    """功能： 初始化服务器
    :return : 返回服务器列表，用于停止服务器
    """

    # web
    logger.info("web server loading")
    web_sockets = tornado.netutil.bind_sockets(options.port)
    app = Application()
    web_server = HTTPServer(app)
    web_server.add_sockets(web_sockets)
    return [web_server]


def shutdown_server_register(server_list, task_list):
    """功能： 正确的关闭服务器，监听服务器关闭信号，开始执行关闭操作
    1、停止接受新的请求
    2、完成正在运行的请求
    3、关闭服务器
    """

    MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 3

    # signal handler's callback
    def shutdown():
        logging.info("Stopping HttpServer...")  # No longer accept new traffic
        for item in server_list + task_list:
            item.stop()

        logging.info("IOLoop Will be Terminate in %s Seconds...", MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
        instance = tornado.ioloop.IOLoop.instance()
        deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

        # recursion for terminate IOLoop.instance()
        def terminate():
            now = time.time()
            if now < deadline:
                instance.add_timeout(now + 1, terminate)
            else:
                instance.stop()
                logging.info("Shutdown...")

        # process recursion
        terminate()

    # signal handler
    def sig_handler(sig, frame):
        logging.warning("Caught Signal: %s", sig)
        tornado.ioloop.IOLoop.instance().add_callback(shutdown)

    # signal register
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)


def main():
    tornado.options.parse_command_line()

    server_list = server_initialize()
    task_list = task_initialize()
    shutdown_server_register(server_list, task_list)

    # tornado.process.fork_processes(0)  # 有多少个CPU，就运行多少个进程
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
