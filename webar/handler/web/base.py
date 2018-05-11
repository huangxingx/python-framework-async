#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:10/05/18
import json

from core.auth.token import TokenManager, PayLoad
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

        payload = PayLoad(**payload)
        user_id = payload.user_id

        user = await self.s_user.get_user_by_id(user_id)

        if user is None:
            return None

        # 比较 last_modify_password_timestamp
        if user.get('last_modify_password_timestamp') and payload.last_modify_password_timestamp < user.get(
                'last_modify_password_timestamp'):
            return None

        return user


class WebHandler(BaseWebHandler):
    pass


class WebAuthHandler(BaseWebHandler, AuthBaseHandler):
    pass
