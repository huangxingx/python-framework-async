#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:08/05/18
from model.test.test_model import TestModel
from model.user.user import WebARUserModel


class ModelMixin(object):
    # todo load model

    m_test = TestModel()
    m_webar_user = WebARUserModel()
