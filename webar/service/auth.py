#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-4
import json
import logging
import typing
from enum import Enum

from core.util import DatetimeJSONEncoder
from model.user.user import WebARUserModel
from service.base import BaseService


class LoginAuthTypeError(Exception):
    pass


class LoginService(BaseService):
    @staticmethod
    def get_user_key(user_id):
        return f'user:{user_id}'

    @staticmethod
    def get_user_token_key(user_id):
        return f'token:user:{user_id}'

    async def auth(self, auth_type, username, password):
        authentication = Authentication.get_login_auth(auth_type)
        user = await authentication.auth(username, password)
        return user

    async def set_user_info_to_cache(self, user, expire):
        """ 把用户对象写入 cache """
        user_id = str(user.get("_id"))
        user_key = self.get_user_key(user_id)
        user = json.dumps(user, cls=DatetimeJSONEncoder)
        await self.cache.setex(user_key, expire, user)

    async def logout(self, user_id):
        """ 推出登录操作 """
        pass


class LoginAuthTypeEnum(Enum):
    api = 'api'
    web = 'web'
    admin = 'web'


class LoginAuth(object):
    async def auth(self, username, password):
        raise NotImplementedError()


class ApiLoginAuth(LoginAuth):
    model = WebARUserModel()

    async def auth(self, username, password) -> typing.Optional[dict]:
        user = await self.model.check_password(username, password)
        return user


class AdminLoginAuth(LoginAuth):
    model = WebARUserModel()

    async def auth(self, username, password) -> typing.Optional[dict]:
        user = await self.model.check_password(username, password)
        return user


class WebLoginAuth(LoginAuth):
    model = WebARUserModel()

    async def auth(self, username, password) -> typing.Optional[dict]:
        user = await self.model.check_password(username, password)
        return user


class Authentication(object):

    @classmethod
    def get_login_auth(cls, auth_type: LoginAuthTypeEnum):
        mapping = {
            LoginAuthTypeEnum.api: ApiLoginAuth,
            LoginAuthTypeEnum.web: WebLoginAuth,
            LoginAuthTypeEnum.admin: AdminLoginAuth,
        }

        if auth_type in mapping:
            return mapping[auth_type]()
        raise LoginAuthTypeError(f'{auth_type} not exist')
