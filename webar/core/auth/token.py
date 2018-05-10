#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

# @author: x.huang
# @date:10/05/18
from jwt import ExpiredSignatureError

import yxexceptions
from core.util import singleton
from .jwe import JwtHelper

__all__ = ['TokenManager', 'TokenResult']


class TokenResult:
    """
    :parameter
        - access_token:
        - refresh_token:
        - access_token_expire:
        - refresh_token_expire:
    """

    def __init__(self,
                 access_token,
                 refresh_token,
                 access_token_expire=None,
                 refresh_token_expire=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.access_token_expire = access_token_expire
        self.refresh_token_expire = refresh_token_expire

    def as_dict(self):
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'access_token_expire': self.access_token_expire,
            'refresh_token_expire': self.refresh_token_expire,
        }


class TokenManager(object):

    def __init__(self, jwt_help):
        """

        :param JwtHelper jwt_help: JwtHelper 对象
        """
        self.jwt_help = jwt_help

    async def parse(self, token, is_refresh_token=False):
        token_type = TokenTypeEnum.AccessToken if not is_refresh_token else TokenTypeEnum.RefreshToken
        validation = TokenValidationFactory.get_instance(token_type)(jwt_help=self.jwt_help)

        return await validation.parse(token)

    def gen_token(self, access_token_expire, refresh_token_expire=None, payload=None) -> TokenResult:
        access_token = self._gen_token(access_token_expire, payload=payload)
        refresh_token = self._gen_token(refresh_token_expire, payload=payload)

        return TokenResult(
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expire=access_token_expire,
            refresh_token_expire=refresh_token_expire,
        )

    def _gen_token(self, expire, payload=None):
        if expire is None:
            return None
        return self.jwt_help.gen_token(payload, expire)


class TokenTypeEnum(Enum):
    AccessToken = 'access_token'
    RefreshToken = 'refresh_token'


class TokenValidationFactory:
    @classmethod
    def get_instance(cls, token_type):
        if token_type == TokenTypeEnum.AccessToken:
            return AccessTokenValidation

        if token_type == TokenTypeEnum.RefreshToken:
            return RefreshTokenValidation


class TokenValidation:

    def __init__(self, jwt_help=None):
        """

        :param JwtHelper jwt_help: JwtHelper 对象
        """
        self.jwt_help = jwt_help

    async def parse(self, token: str):
        """ 验证token 是否可用 """
        pay_load, err = self.jwt_help.parse_token(token)

        if err is ExpiredSignatureError:
            self.on_expire_error()

        elif err:
            raise yxexceptions.TokenInvalidException
        return pay_load

    def on_expire_error(self):
        """ token过期的操作 """

        raise NotImplementedError


@singleton
class AccessTokenValidation(TokenValidation):

    def on_expire_error(self):
        raise yxexceptions.AccessTokenExpireException


@singleton
class RefreshTokenValidation(TokenValidation):

    def on_expire_error(self):
        raise yxexceptions.RefreshTokenExpireException
