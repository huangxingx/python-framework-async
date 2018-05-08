#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-16
import typing
import motor
from motor.motor_tornado import MotorCursor
from pymongo.results import InsertOneResult, InsertManyResult, DeleteResult, UpdateResult
from tornado import options

IS_DELETE = 'is_delete'


class BaseModel(object):
    _collection_ = ''

    def __init__(self):
        """ 调用初始化索引 """
        self.init_index()

    def init_index(self):
        """ 初始化索引 """
        pass

    @property
    def _database_(self):
        return self.__module__.split('.')[1]

    @property
    def db(self):
        """ mongodb 实例 """
        return options.options['mongodb']  # type: motor.MotorClient

    @property
    def _dao(self):
        """ 集合 实例 """
        return self.db[self._database_][self._collection_]

    async def find_one(self, spec):
        self._add_delete_flag(spec)
        r = await self._dao.find_one(spec)
        return r

    async def insert_one(self, document) -> typing.Optional[str]:
        """

        :param document: 需要插入的数据
        :return: str or None
        """
        r = await self._dao.insert_one(document)  # type: InsertOneResult
        return str(r.inserted_id) if r else None

    async def insert_many(self, document_list) -> typing.List[str]:
        """ 批量插入 """

        r = await self._dao.insert_many(document_list)  # type: InsertManyResult
        return [str(_id) for _id in r.inserted_ids] if r else None

    async def find(self, spec, projection=None, sort=None, skip=0, limit=0) -> MotorCursor:
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
        return await self._dao.update(spec, document, upsert=upsert, manipulate=manipulate,
                                      multi=multi)  # type: UpdateResult

    async def get_list(self, spec, projection=None, sort=None, skip=0, limit=0, length=0):
        """ 获取列表

        :param dict spec: 过滤条件
        :param list projection: 返回字段， exclude use [{'_id': False}]
        :param list sort: 排序  [(filed, direction)]
        :param skip:
        :param limit: 查询时返回条数
        :param length: 返回列表长度
        :return:
        """
        cursor = await self.find(spec, projection, sort=sort, skip=skip, limit=limit)
        return await cursor.to_list(length=length)

    @staticmethod
    def _add_delete_flag(spec: dict) -> dict:
        if IS_DELETE not in spec:
            spec[IS_DELETE] = 0
        return spec
