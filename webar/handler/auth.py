#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-4

import logging
import typing
from enum import Enum

from handler.base import BaseRequestHandler
from yxexceptions import LoginRequireException

__all__ = ['Authentication', 'LoginAuthTypeEnum', 'AuthBaseHandler']


class AuthBaseHandler(BaseRequestHandler):
    """ 登录验证的基类 """

    async def prepare(self):
        self.current_user = await self.get_current_user()
        if not self.current_user and self.request.method.lower() != 'options':
            self.render_error(msg=LoginRequireException.error_msg, error_code=LoginRequireException.error_code)
            return
        super(AuthBaseHandler, self).prepare()


class LoginAuthTypeError(Exception):
    pass


class LoginAuthTypeEnum(Enum):
    api = 'api'
    web = 'web'
    admin = 'web'


class LoginAuth(object):
    def __init__(self, model):
        self.model = model

    async def auth(self, username, password):
        raise NotImplementedError()


class ApiLoginAuth(LoginAuth):
    async def auth(self, username, password) -> typing.Optional[dict]:
        user, err = await self.model.check_password(username, password)
        return user


class AdminLoginAuth(LoginAuth):
    async def auth(self, username, password) -> typing.Optional[dict]:
        user = await self.model.check_password(username, password)
        return user


class WebLoginAuth(LoginAuth):
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
            return mapping[auth_type]
        raise LoginAuthTypeError(f'{auth_type} not exist')
