#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:07/05/18

import logging
import os
import sys

import tornado
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.tornado import TornadoScheduler
from tornado import ioloop, gen
from tornado import web
from tornado.options import define
from tornado.options import options
from tornado.options import parse_command_line
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

# 初始化环境
file_path = os.path.realpath(__file__)
project_dir = os.path.dirname(file_path)
os.chdir(project_dir)
sys.path.append(project_dir)

# 必须在环境变量加载后引包
import setting
from core import util
from urls import urls

# define
define("port", default=7777, help="Run server on a specific port", type=int)


# start code

class Application(web.Application):
    executor = ThreadPoolExecutor()

    def __init__(self):
        handler_list = urls
        settings = dict(
            debug=setting.DEBUG,
        )

        web.Application.__init__(self, handler_list, **settings)


def server_start():
    app = Application()
    options.logging = 'info'
    parse_command_line()
    app.listen(options.port)
    io_loop = ioloop.IOLoop.current()

    # todo add callback

    try:
        logging.info('Tornado version {}'.format(tornado.version))
        logging.info('Tornado Server Start, listen on {}'.format(options.port))
        logging.info('Quite the Server with CONTROL-C.')
        io_loop.start()
    except KeyboardInterrupt:
        io_loop.close()


if __name__ == '__main__':
    server_start()
