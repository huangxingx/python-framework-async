#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:10/05/18
import json

from core.auth.token import TokenManager
from yxexceptions import YXException
from ..auth import AuthBaseHandler
from ..base import BaseRequestHandler


class BaseWebHandler(BaseRequestHandler):
    async def get_current_user(self):
        if self.token is None:
            return None

        token_manager = TokenManager(self.application.jwt_helper)
        payload = await token_manager.parse(self.token)

        if not payload:
            return None

        user_id = payload.get('user_id')
        user_key = f'user:{user_id}'

        user = await self.cache.get(user_key)

        if user is None:
            return None

        user = json.loads(user)
        return user


class WebHandler(BaseWebHandler):
    pass


class WebAuthHandler(BaseWebHandler, AuthBaseHandler):
    pass
