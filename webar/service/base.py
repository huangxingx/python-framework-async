#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:08/05/18

from tornado import gen

from service.modelmixin import ModelMixin


class BaseService(ModelMixin):

    async def find_one(self, spec=None):
        if spec is None:
            spec = {}
        r = await self.m_test.find_one(spec)
        return r
