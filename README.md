# 框架源码 #

* config > 环境配置文件， sql/mq/redis

* handler > 业务逻辑的 handlers， 只能调用services层操作数据，不能直接调用models层.

* core > 库文件 ， 日志模块， 加载器（加载sql， session， memcache），

* model > 数据库表的实体类 orm 映射类

* service > 存储过程抽象层
