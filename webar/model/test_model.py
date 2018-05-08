#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:08/05/18
from model import BaseModel


class TestModel(BaseModel):
    """ 测试  """

    _collection_ = 'test1'
    _database_ = 'test'
