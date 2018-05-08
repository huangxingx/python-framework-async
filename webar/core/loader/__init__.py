#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:07/05/18

from .mongodb import MongoDB
from .rabbitmq import *
from .redis import *


class LoadError(Exception):
    pass


class Loader(object):
    mapping = {
        'mongodb': MongoDB,
        'aioredis': AioRedis,
        'rabbitmq': Rabbitmq,
    }

    @classmethod
    def load(cls, name: str, **kwargs):
        if name not in cls.mapping:
            return LoadError(f'load {name} error, {name} not exists')
        instance = cls.mapping.get(name)().load(**kwargs)
        return instance

    @classmethod
    async def async_load(cls, name: str, **kwargs):
        if name not in cls.mapping:
            return LoadError(f'load {name} error, {name} not exists')
        instance = await cls.mapping.get(name)().load(**kwargs)
        return instance
