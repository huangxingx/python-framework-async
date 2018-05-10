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

    async def write_token_info_to_cache(self, token_result, user):
        user_id = str(user.get("_id"))
        user_tokens_key = self.get_user_token_key(user_id)
        user_key = self.get_user_key(user_id)

        pipe = self.cache.pipeline()
        user = json.dumps(user, cls=DatetimeJSONEncoder)
        pipe.setex(user_key, token_result.access_token_expire, user)

        pipe.hset(user_tokens_key, token_result.access_token, token_result.refresh_token)
        await pipe.execute()

    async def logout(self, user_id, token):
        user_tokens_key = self.get_user_token_key(user_id)

        await self.cache.hdel(user_tokens_key, token)
        num = await self.cache.hlen(user_tokens_key)
        if not int(num):
            user_key = self.get_user_key(user_id)
            await self.cache.delete(user_key)


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
