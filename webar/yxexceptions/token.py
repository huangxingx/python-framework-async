#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:10/05/18

from .base import YXException

AccessTokenExpireException = YXException(1101, 'AccessTokenExpireException')
AccessTokenNotExistException = YXException(1102, 'AccessTokenNotExistException')

RefreshTokenExpireException = YXException(1103, 'RefreshTokenExpireException')
RefreshTokenNotExistException = YXException(1104, 'RefreshTokenNotExistException')

TokenInvalidException = YXException(1105, 'TokenInvalidException')
