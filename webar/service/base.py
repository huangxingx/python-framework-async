#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:08/05/18
import redis
from tornado import options

from service.modelmixin import ModelMixin


class BaseService(ModelMixin):
    @property
    def cache(self) -> redis.Redis:
        """ 缓存对象 TornadoScheduler """

        return options.options['redis_client']
