#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:08/05/18

from handler.base import BaseRequestHandler, ListResult


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
        # r = await self.s_test.m_test.distinct('post', {'_id': '5af16be7d9d74d34e4906ab7'})
        # r = await self.s_test.m_test.find_one({'_id': '5af16be7d9d74d34e4906ab7'})
        r = await self.s_test.m_test.get_page_list(page=1, page_size=2)
        toekn, err = self.parse_token()
        result = ListResult(data_list=r, count=len(r))
        self.render_success(result)

    async def _post(self, *args, **kwargs):

        insert_data = self.request.json
        if isinstance(insert_data, list):
            r = await self.s_test.m_test.insert_many(insert_data)
        else:
            r = await self.s_test.insert_one(insert_data)
        self.render_success(r)

    async def _delete(self, *args, **kwargs):
        is_many = self.get_argument('is_many', False)
        delete_spec = {'_id': '5af16be7d9d74d34e4906ab7'}

        delete_count = await self.s_test.m_test.delete(delete_spec, is_many)
        self.render_success(delete_count)

    async def _put(self, *args, **kwargs):
        update_date = self.request.json
        spec_data = {'_id': '5af16be7d9d74d34e4906ab7'}
        r = await self.s_test.m_test.update(spec_data, update_date, multi=False)
        self.render_success(r)
