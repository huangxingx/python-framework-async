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
from motor import MotorClient
from tornado import ioloop
from tornado import web
from tornado.options import define
from tornado.options import options
from tornado.options import parse_command_line

# 初始化环境
file_path = os.path.realpath(__file__)
project_dir = os.path.dirname(file_path)
os.chdir(project_dir)
sys.path.append(project_dir)

# 必须在环境变量加载后引包
import setting
from core import util
from core import loader
from core.auth.jwe import JwtHelper

# define
define("port", default=7777, help="Run server on a specific port", type=int)
define("mq_connection", default=None, help="mq connection", type=pika.adapters.tornado_connection.TornadoConnection)
define("mongodb", default=None, help="mq connection", type=motor.MotorClient)
define("redis_client", default=None, help="mq connection", type=aioredis.commands.Redis)


# start code

class Application(web.Application):

    def __init__(self):
        handler_list = util.import_object('urls.urls')
        settings = dict(
            debug=setting.DEBUG,
        )

        # jwt 对象
        self.jwt_helper = JwtHelper()

        web.Application.__init__(self, handler_list, **settings)


async def ping_mongodb(db):
    """ 测试mongodb的连通性，并打印出版本信息 """

    try:
        version_info = await db.admin.system.version.find_one({})
        options['mongodb'] = db
    except Exception:
        logging.error('mongodb load fail', exc_info=True)
        sys.exit(1)
    else:
        logging.info(f"load mongodb success, mongo info: {version_info}")


async def load_redis():
    """ 异步加载 hiredis """

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

    # loader
    logging.info(f'start connect mongodb {setting.MONGO_CONF.get("host")}:{setting.MONGO_CONF.get("port")}')
    db = loader.Loader.load('mongodb', **setting.MONGO_CONF)  # type: MotorClient

    # 加载rabbitmq
    loader.Loader.load('rabbitmq', **setting.RABBITMQ_CONF)

    io_loop = ioloop.IOLoop.current()

    # todo add callback
    io_loop.add_callback(ping_mongodb, db)  # 测试 mongodb
    io_loop.add_callback(load_redis)  # 异步加载 redis client

    # application 实例
    app = Application()
    app.listen(options.port)

    try:
        logging.info('Tornado version {}'.format(tornado.version))
        logging.info('Tornado Server Start, listen on {}'.format(options.port))
        logging.info('Quite the Server with CONTROL-C.')
        io_loop.start()
    except KeyboardInterrupt:
        io_loop.close()


if __name__ == '__main__':
    server_start()
