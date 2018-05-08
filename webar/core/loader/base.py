#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:07/05/18


class AbstractLoader(object):
    @classmethod
    def load(cls, **kwargs):
        """ 加载系统所需服务 如 mongo redis

        :param kwargs: 可选参数
        :return: 服务实例
        """
        raise NotImplementedError()
