#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:08/05/18
from service.test_service import TestService
from service.auth import LoginService


class ServiceMixin(object):
    s_test = TestService()

    s_login = LoginService()
