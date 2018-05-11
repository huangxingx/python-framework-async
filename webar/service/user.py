#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:11/05/18
import json

from service.base import BaseService


class UserService(BaseService):
    """ 所有 User Service  admin user and web user """

    @staticmethod
    def get_user_key(user_id):
        return f'user:{str(user_id)}'

    async def get_user_by_id(self, user_id, is_admin=False):
        # get from cache
        user_key = self.get_user_key(user_id)
        user = await self.cache.get(user_key)
        if user:
            user = json.loads(user)
            return user

        # get user from db
        user_model = self.m_webar_user if not is_admin else self.m_webar_user  # todo 改为admin user model
        user = await user_model.find_one(user_id)
        return user
