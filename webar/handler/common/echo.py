#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:07/05/18

from tornado import gen

from handler.base import BaseRequestHandler


class EchoHandler(BaseRequestHandler):
    @gen.coroutine
    def _get(self, *args, **kwargs):
        self.render_success('hello, world')
