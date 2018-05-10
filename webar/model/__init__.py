#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-16
import time
import typing

import bson
import motor
from motor.motor_tornado import MotorCursor
from pymongo.results import InsertOneResult, InsertManyResult, DeleteResult, UpdateResult
from tornado import options

IS_DELETE = 'is_delete'
CREATE_TIME = 'create_time'
LAST_MODIFY = 'last_modify'
DEFAULT_PAGE_SIZE = 20


def translate_id_to_object_id(_id):
    if isinstance(_id, str):
        return bson.ObjectId(_id)
    return _id


def parse_spec_id_to_object_id(spec: typing.Union[dict, str]) -> typing.Union[dict, bson.ObjectId]:
    if isinstance(spec, dict):
        if '_id' in spec and isinstance(spec['_id'], str):
            spec['_id'] = translate_id_to_object_id(spec['_id'])
    elif isinstance(spec, str):
        return translate_id_to_object_id(spec)
    return spec


def add_create_info(document):
    """ 添加创建基本信息 """
    if CREATE_TIME not in document:
        document[CREATE_TIME] = int(time.time())

    if LAST_MODIFY not in document:
        document[LAST_MODIFY] = int(time.time())

    return document


def update_last_modify(document):
    """ 更新 last_modify """

    update_date = document.get("$set", None)
    if update_date:
        update_date[LAST_MODIFY] = int(time.time())
    else:
        document[LAST_MODIFY] = int(time.time())
    return document


class BaseModel(object):
    _collection_ = ''
    _prefix_database_ = 'webar'

    def __init__(self):
        """ 调用初始化索引 """
        self.init_index()

    def init_index(self):
        """ 初始化索引 """
        pass

    @property
    def _database_(self):
        return '%s_%s' % (self._prefix_database_, self.__module__.split('.')[1])

    @property
    def db(self):
        """ mongodb 实例 """
        return options.options['mongodb']  # type: motor.MotorClient

    @property
    def _dao(self):
        """ 集合 实例 """
        return self.db[self._database_][self._collection_]

    async def find_one(self, spec):
        """ 返回一条数据 """
        self._add_delete_flag(spec)  # 添加逻辑删除条件
        spec = parse_spec_id_to_object_id(spec)
        r = await self._dao.find_one(spec)
        return r

    async def insert_one(self, document) -> typing.Optional[str]:
        """ 插入一条数据

        :param document: 需要插入的数据
        :return: str or None
        """
        add_create_info(document)

        r = await self._dao.insert_one(document)  # type: InsertOneResult
        return str(r.inserted_id) if r else None

    async def insert_many(self, document_list) -> typing.List[str]:
        """ 批量插入 """
        new_document_list = map(add_create_info, document_list)

        r = await self._dao.insert_many(new_document_list)  # type: InsertManyResult
        return [str(_id) for _id in r.inserted_ids] if r else None

    async def find(self, spec, projection=None, sort=None, skip=0, limit=0) -> MotorCursor:
        """ 返回 Cursor 对象 """
        return self._dao.find(spec, projection=projection, sort=sort, skip=skip, limit=limit)

    async def delete(self, spec_or_id, delete_many=True, is_logic_delete=True) -> int:
        """ 逻辑删除和物理删除

        :param str|dict spec_or_id: 过滤条件
        :param bool delete_many: 是否操作多条记录 ，默认是
        :param bool is_logic_delete: 是否逻辑删除，默认是
        :return:
        """
        if is_logic_delete:
            update_result = await self.update(spec_or_id, {'$set': {IS_DELETE: 1}})
            return update_result.modified_count

        if delete_many:
            r = await self._dao.delete_many(spec_or_id)  # type: DeleteResult
        else:
            r = await self._dao.delete_one(spec_or_id)
        return r.deleted_count

    async def update(self, spec, document, upsert=False, manipulate=False, multi=True) -> UpdateResult:
        """ 更新操作

        :param spec: 过滤条件
        :param document: 更新的内容
        :param bool upsert: If True, perform an insert if no documents match the filter.
        :param manipulate:
        :param multi: 是否操作多条记录
        :return:
        """
        spec = parse_spec_id_to_object_id(spec)
        self._add_delete_flag(spec)

        update_last_modify(document)

        return await self._dao.update(spec, document, upsert=upsert, manipulate=manipulate,
                                      multi=multi)  # type: UpdateResult

    async def get_list(self, spec=None, projection=None, sort=None, skip=0, limit=0, length=None):
        """ 获取列表

        :param dict spec: 过滤条件
        :param list projection: 返回字段， exclude use [{'_id': False}]
        :param list sort: 排序  [(filed, direction)]
        :param skip:
        :param limit: 查询时返回条数
        :param length: 返回列表长度
        :return: list of this collection
        """
        if spec is None:
            spec = {}
        spec = parse_spec_id_to_object_id(spec)

        cursor = await self.find(spec, projection, sort=sort, skip=skip, limit=limit)
        return await cursor.to_list(length=length)

    async def get_page_list(self, spec=None, projection=None, sort=None, page=0, page_size=DEFAULT_PAGE_SIZE):
        """ 获取分页列表 """

        if spec is None:
            spec = {}
        skip = page * page_size
        return await self.get_list(spec, projection=projection, sort=sort, skip=skip, length=page_size)

    async def count(self, spec=None, is_contain_delete=False) -> int:
        """ a number of this connection

        :param dict|id spec: 查询条件
        :param bool is_contain_delete: 是否包含逻辑删除
        :return: int,
        """
        spec = parse_spec_id_to_object_id(spec)
        if spec is None:
            spec = {}
        if not is_contain_delete:
            spec[IS_DELETE] = {'$ne': 1}

        return await self._dao.count(spec)

    async def distinct(self, key, spec=None) -> list:
        """ 获取去重之后的列表

        :param str key: 返回的字段
        :param dict spec: 过滤的条件
        :return: list
        """
        spec = parse_spec_id_to_object_id(spec)

        self._add_delete_flag(spec)
        return await self._dao.distinct(key, spec)

    @staticmethod
    def _add_delete_flag(spec: typing.Optional[dict]) -> typing.Optional[dict]:
        if spec and IS_DELETE not in spec:
            spec[IS_DELETE] = {'$ne': 1}

        return spec


class BaseUserModel(object):
    async def check_password(self, username, password):
        raise NotImplementedError()

    def gen_password(self):
        pass


class UserNotExistError(Exception):
    pass


class PasswordError(Exception):
    pass
