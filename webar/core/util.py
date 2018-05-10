#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-1


from __future__ import absolute_import, division, with_statement

import datetime
import decimal
import json
from abc import ABCMeta
from functools import wraps

from bson import ObjectId


class ObjectDict(dict):
    """Makes a dictionary behave like an object."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


def import_object(name):
    """Imports an object by name.

    import_object('x.y.z') is equivalent to 'from x.y import z'.
    """
    parts = name.split('.')
    obj = __import__('.'.join(parts[:-1]), None, None, [parts[-1]], 0)
    return getattr(obj, parts[-1])


def import_package(name):
    obj = __import__(name)
    return obj


class DatetimeJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime,)):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        elif isinstance(obj, (decimal.Decimal,)):
            return float(obj)

        elif isinstance(obj, bytes):
            return obj.decode('utf-8')

        elif isinstance(obj, ObjectId):
            return str(obj)
        else:
            return super(DatetimeJSONEncoder, self).default(obj)


class AbstractBase(object):
    __metaclass__ = ABCMeta


class RedisLock(object):
    from redis import Redis

    def __init__(self, redis_client: Redis, lock_name):
        self.redis_client = redis_client
        self.lock_name = lock_name

    def release(self):
        self.redis_client.delete(self.lock_name)

    def acquire(self):
        lock_value = self.redis_client.incr(self.lock_name)
        if lock_value == 1:
            self.redis_client.expire(self.lock_name, 60)
            return True
        else:
            return False


def singleton(cls):
    instance = {}

    @wraps(cls)
    def _singleton(*args, **kw):
        if cls not in instance:
            instance[cls] = cls(*args, **kw)
        return instance[cls]

    return _singleton
