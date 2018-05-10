#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:18-1-3

"""
BaseApiHandler： Api的基类
ApiHandler: Api 不带登录验证的基类
ApiAuthHandler: Api 带登录验证的基类

"""
from yxexceptions import YXException
from ..auth import AuthBaseHandler
from ..base import BaseRequestHandler


class BaseApiHandler(BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseApiHandler, self).__init__(*args, **kwargs)
        self.appuser = self.session.get('appuser')

    def prepare(self):
        try:
            super(BaseApiHandler, self).prepare()
        except YXException as e:
            self.render_error(str(e.error_msg), error_code=e.error_code)

    def get_current_user(self):
        if not self.appuser:
            return None
        phone = self.appuser.get('phone')
        if phone:
            return phone
        else:
            return None


class ApiHandler(BaseApiHandler):
    pass


class ApiAuthHandler(BaseApiHandler, AuthBaseHandler):
    pass
