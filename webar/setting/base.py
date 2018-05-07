#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-2

from core import load_config

env_ini = load_config.get_config_by_name('env')
db_ini = load_config.get_config_by_name('db')

_session_conf = db_ini['session']
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
SQL_PORT = _db_conf.get('port', 27017)
SQL_HOST = _db_conf.get('host', '127.0.0.1')
SQL_USER = _db_conf.get('user')
SQL_PASSWORD = _db_conf.get('pass')
