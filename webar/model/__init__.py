#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-16
import motor
from tornado import options
from tornado import gen


class BaseModel(object):
    _database_ = ''
    _collection_ = ''

    def __init__(self):
        """ 调用初始化索引 """
        self.init_index()

    def init_index(self):
        """ 初始化索引 """
        pass

    @property
    def db(self):
        """ mongodb 实例 """
        return options.options['mongodb']  # type: motor.MotorClient

    @property
    def _dao(self):
        """ 集合 实例 """
        return self.db[self._database_][self._collection_]

    async def find_one(self, spec):
        r = await self._dao.find_one(spec)
        return r

    def find_all(self):
        pass

    def get_list(self):
        pass
