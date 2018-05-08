#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:08/05/18

from handler.base import BaseRequestHandler


class RedisTestHandler(BaseRequestHandler):
    async def _get(self, *args, **kwargs):
        test_key = 'test:1'
        old = await self.cache.get(test_key)
        await self.cache.set(test_key, 'huangxing')
        new = await self.cache.get(test_key)
        await self.cache.delete(test_key)
        self.render_success({
            'old': old,
            'new': new,
        })


class MongoTestHandler(BaseRequestHandler):

    async def _get(self, *args, **kwargs):
        r = await self.s_test.find_one()
        self.render_success(r)
