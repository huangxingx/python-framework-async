#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:10/05/18
from core.md5 import gen_md5
from model import BaseModel
from model import BaseUserModel
from model import UserNotExistError, PasswordError


class WebARUserModel(BaseModel, BaseUserModel):
    _collection_ = 'webar_user'

    user_name = 'user_name'
    email_address = 'email_address'
    pwd = 'pwd'
    phone = 'phone'
    permission_id = 'permission_id'

    async def check_password(self, username, input_password):
        query = {
            self.user_name: username,
        }

        user = await self.find_one(query)
        if user:
            raw_password = user.get(self.pwd)
            if raw_password == gen_md5(input_password):
                return user
            raise PasswordError('password error')
        raise UserNotExistError(f'user not exist, username: {username}')
