#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:07/05/18
import sys
import logging
from .base import AbstractLoader
import aioredis


class AioRedis(AbstractLoader):
    _redis_pool = None

    @classmethod
    async def load(cls, **kwargs):
        address = kwargs.pop('address')
        port = kwargs.pop('port')

        address_url = f'redis://{address}:{port}'
        if not cls._redis_pool:
            try:
                cls._redis_pool = await aioredis.create_redis_pool(address_url, **kwargs)
            except Exception:
                # redis 连接失败 退出程序
                logging.error('redis connect fail.', exc_info=True)
                sys.exit(1)
        return cls._redis_pool
