#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:18-1-12


class YXException(BaseException):

    def __init__(self, error_code=0, error_msg=''):
        self.error_code = error_code
        self.error_msg = error_msg
