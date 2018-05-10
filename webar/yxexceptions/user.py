#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:10/05/18

from .base import YXException

UsernameAndPasswordNotMatchException = YXException(1201, '用户名密码不匹配')
UserNotExistsException = YXException(1202, '用户不存在')
