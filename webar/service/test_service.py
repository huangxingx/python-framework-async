#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:08/05/18

from service.base import BaseService


class TestService(BaseService):
    async def find_one(self, spec=None):
        if spec is None:
            spec = {}
        r = await self.m_test.find_one(spec)
        return r

    async def get_list(self, spec=None, length=None):
        if spec is None:
            spec = {}
        r = await self.m_test.get_list(spec, length=length)
        return r

    async def insert_one(self, document=None):
        if document is None:
            return None
        r = await self.m_test.insert_one(document)
        return r
