#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:10/05/18

import setting
import yxexceptions
from core.auth.token import TokenManager
from handler.web.base import WebHandler
from model import UserNotExistError, PasswordError
from service.auth import LoginAuthTypeEnum


class WebLoginHandler(WebHandler):

    async def _post(self):
        """ webar 创建用户登录 认证 """

        account = self.get_json_data('account', arg_type=str)
        password = self.get_json_data('pwd', arg_type=str)
        try:
            user = await self.s_login.auth(LoginAuthTypeEnum.web, account, password)

        except UserNotExistError:
            raise yxexceptions.UserNotExistsException

        except PasswordError:
            raise yxexceptions.UsernameAndPasswordNotMatchException

        # 生成 token对象
        user_id = str(user.get('_id'))
        token_result = TokenManager(self.application.jwt_helper).gen_token(setting.ACCESS_TOKEN_EXPIRE,
                                                                           setting.REFRESH_TOKEN_EXPIRE,
                                                                           payload={'user_id': user_id})
        # 认证信息 写入 cache
        await self.s_login.write_token_info_to_cache(token_result, user)

        self.render_success(token_result.as_dict())

    async def _get(self, *args, **kwargs):
        user = await self.get_current_user()
        self.render_success(user)

    async def _delete(self, *args, **kwargs):
        user = await self.get_current_user()
        if user is None:
            self.render_success()
            return
        user_id = user.get('_id')
        await self.s_login.logout(user_id, self.token)
        self.render_success()
