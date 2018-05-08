#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:07/05/18
import motor

from .base import AbstractLoader


class MongoDB(AbstractLoader):

    _instance = None

    @classmethod
    def load(cls, host='127.0.0.1', port=27017, username=None, password=None, **kwargs):
        if not cls._instance:
            cls._instance = motor.MotorClient(host=host, port=port, username=username, password=password, **kwargs)
        return cls._instance
