#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:07/05/18
import setting
from handler import web
from handler import api
from handler import admin
from handler import common

from handler.test import *

admin_url = [
    (r'/admin/echo', common.EchoHandler)
]

web_url = [
    (r'/web/echo', common.EchoHandler)
]

api_url = [
    (r'/api/echo', common.EchoHandler)

]

test_url = [
    ('/test/redis', RedisTestHandler),
    ('/test/mongo', MongoTestHandler)
]

urls = admin_url + web_url + api_url

if setting.DEBUG:
    urls += test_url

if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.INFO)
    api_url_len = len(api_url)
    web_url_len = len(web_url)
    admin_url_len = len(admin_url)
    logging.info('api url: %d' % api_url_len)
    logging.info('admin url: %d' % admin_url_len)
    logging.info('web url: %d' % web_url_len)
    logging.info('total url: %d' % (web_url_len + admin_url_len + api_url_len))
