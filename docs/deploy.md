## 部署环境 ##

#### 软件工具 ####
* ubuntu 14.04
* Python 3.6.4
* Redis 2.8.9
* Nginx 1.10.1
* Rabbitmq 3.6.10


### 初始化项目 ###
1. 修改 gather_city/config/db.ini 配置文件，改好数据库配置;
2. 修改 gather_city/scripts/init.sh 中 env_path 变量;
2. 执行 gather_city/scripts/init.sh ;


###  配置文件说明 ###
* 详情请参见 /webar/config/readme.md


### 系统启动程序  ###
1. manage.py 为系统的主程序; 默认端口为8383

   ```
   python manage.py --port=8080
   ```


