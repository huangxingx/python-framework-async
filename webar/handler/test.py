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
        r = await self.s_test.get_list(length=1)
        self.render_success(r)

    async def _post(self, *args, **kwargs):

        insert_data = self.request.json
        if isinstance(insert_data, list):
            r = await self.s_test.m_test.insert_many(insert_data)
        else:
            r = await self.s_test.insert_one(insert_data)
        self.render_success(r)

    async def _delete(self, *args, **kwargs):
        is_many = self.get_argument('is_many', False)
        delete_spec = {"post": "test"}

        delete_count = await self.s_test.m_test.delete(delete_spec, is_many)
        self.render_success(delete_count)

    async def _put(self, *args, **kwargs):
        update_date = self.request.json
        spec_data = {"post1" : "test1"}
        r = await self.s_test.m_test.update(spec_data, update_date, multi=False)
        self.render_success(r)