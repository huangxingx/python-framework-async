#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:07/05/18

import logging
import os
import sys

import aioredis
import motor
import pika
import tornado
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.tornado import TornadoScheduler
from motor import MotorClient
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
from core import loader

# define
define("port", default=7777, help="Run server on a specific port", type=int)
define("mq_connection", default=None, help="mq connection", type=pika.adapters.tornado_connection.TornadoConnection)
define("mongodb", default=None, help="mq connection", type=motor.MotorClient)
define("redis_client", default=None, help="mq connection", type=aioredis.commands.Redis)


# start code

class Application(web.Application):
    executor = ThreadPoolExecutor()

    def __init__(self):
        handler_list = urls
        settings = dict(
            debug=setting.DEBUG,
        )

        web.Application.__init__(self, handler_list, **settings)


@gen.coroutine
def ping_mongodb(db):
    """ 测试mongodb的连通性，并打印出版本信息 """
    try:
        version_info = yield db.admin.system.version.find_one({})
        options['mongodb'] = db
    except Exception:
        logging.error('mongodb load fail', exc_info=True)
        sys.exit(1)
    else:
        logging.info(f"load mongodb success, mongo info: {version_info}")


async def load_redis(app):
    redis_conf = {
        'address': setting.CACHE_HOST,
        'port': setting.CACHE_PORT,
    }
    logging.info(f'start connect redis {redis_conf}')
    redis_client = await loader.Loader.async_load('aioredis', **redis_conf)
    options['redis_client'] = redis_client
    logging.info('load redis success')


def server_start():
    options.logging = 'info'

    parse_command_line()

    app = Application()

    # loader
    logging.info(f'start connect mongodb {setting.MONGO_CONF.get("host")}:{setting.MONGO_CONF.get("port")}')
    db = loader.Loader.load('mongodb', **setting.MONGO_CONF)  # type: MotorClient
    app.db = db

    loader.Loader.load('rabbitmq', url='amqp://guest:guest@localhost:5672/%2F')

    app.listen(options.port)
    io_loop = ioloop.IOLoop.current()

    # todo add callback
    io_loop.add_callback(ping_mongodb, db)  # 测试 mongodb
    io_loop.add_callback(load_redis, app)  # 异步加载 redis client

    try:
        logging.info('Tornado version {}'.format(tornado.version))
        logging.info('Tornado Server Start, listen on {}'.format(options.port))
        logging.info('Quite the Server with CONTROL-C.')
        io_loop.start()
    except KeyboardInterrupt:
        io_loop.close()


if __name__ == '__main__':
    server_start()
