#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:18-1-12
from .base import YXException

LoginRequireException = YXException(403, 'LoginRequireException: Auth Error.')

CommonException = YXException(1000, 'CommonException.')
