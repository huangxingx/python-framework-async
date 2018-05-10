#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-2

from core import load_config

env_ini = load_config.get_config_by_name('env')
db_ini = load_config.get_config_by_name('db')

_db_conf = db_ini['db']
_cache_conf = db_ini['cache']
_common_conf = env_ini['common']
_rabbitmq_conf = db_ini['rabbitmq']

# 环境
ENV = _common_conf.get('env', 'develop')

# tornado Debug
_is_debug = _common_conf.get('debug', 'False')
if _is_debug == 'True':
    DEBUG = True
else:
    DEBUG = False

# mongodb 配置
SQL_PORT = int(_db_conf.get('port', 27017))
SQL_HOST = _db_conf.get('host', '127.0.0.1')
SQL_USER = _db_conf.get('user') if _db_conf.get('user') else None
SQL_PASSWORD = _db_conf.get('pass') if _db_conf.get('pass') else None
MONGO_CONF = {
    'host': SQL_HOST,
    'port': SQL_PORT,
    'username': SQL_USER,
    'password': SQL_PASSWORD,
}

# cache 配置
CACHE_HOST = _cache_conf.get('host', '127.0.0.1')
CACHE_PORT = int(_cache_conf.get('port', '6379'))

# rabbitmq 中间件配置
RABBITMQ_USER = _rabbitmq_conf.get('user', 'guest')
RABBITMQ_PASS = _rabbitmq_conf.get('pass', 'guest')
RABBITMQ_HOST = _rabbitmq_conf.get('host', '127.0.0.1')
RABBITMQ_PORT = _rabbitmq_conf.get('port', '5672')

RABBITMQ_CONF = {
    'host': RABBITMQ_HOST,
    'port': RABBITMQ_PORT,
    'username': RABBITMQ_USER,
    'password': RABBITMQ_PASS,
}

# 认证过期时间
ACCESS_TOKEN_EXPIRE = 60 * 60 * 24 * 7
REFRESH_TOKEN_EXPIRE = 60 * 60 * 24 * 30
