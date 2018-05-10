#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:09/05/18
import time
import jwt

from core.util import singleton

DEFAULT_EXPIRE = 60 * 60 * 60


@singleton
class JwtHelper(object):
    SECRET = "arhieason"
    ALG = 'HS256'
    ISS = 'arhieason.com'

    def __init__(self, expire=None):
        self._expire = DEFAULT_EXPIRE if expire is None else expire
        self._secret = JwtHelper.SECRET
        self._alg = JwtHelper.ALG
        self._iss = JwtHelper.ISS

    def gen_token(self, payload: dict, expire=None) -> str:
        if expire is None:
            expire = self._expire
        new_payload = {
            "iss": self.ISS,
            "iat": int(time.time()),
            "exp": int(time.time()) + expire,
        }
        if payload is not None:
            new_payload.update(payload)

        token = jwt.encode(new_payload, self._secret, algorithm=self._alg)
        return token

    def parse_token(self, token_str) -> (dict, Exception):
        """

        :param token_str:
        :return:
        :raises: ExpiredSignatureError
                 InvalidTokenError
        """
        try:
            payload = jwt.decode(token_str, self.SECRET, algorithms=[self.ALG])

        except Exception as e:
            return None, e

        return payload, None

    def set_secret(self, secret):
        self._secret = secret

    def set_alg(self, alg):
        self._alg = alg

    def set_iss(self, iss):
        self._iss = iss


if __name__ == '__main__':
    jwt_helper = JwtHelper()
    pay_load, err = jwt_helper.parse_token(
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcmhpZWFzb24uY29tIiwiaWF0IjoxNTI1OTM3NzQ5LCJleHAiOjE1Mjg1Mjk3NDl9.NcJULZxV2wZP8akgHnS3JkvWjjtTvNEqt-88RsRFCW8")
    print(pay_load)
