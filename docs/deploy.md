## 部署环境 ##

#### 软件工具 ####
* ubuntu 14.04
* Python 3.6.4
* Redis 2.8.9
* Nginx 1.10.1
* Rabbitmq 3.6.10


### 初始化项目 ###
1. 修改 webar/config/db.ini 配置文件，改好数据库配置;



###  配置文件说明 ###
* 详情请参见 /webar/config/README.md


### 系统启动程序  ###
1. manage.py 为系统的主程序; 默认端口为 7777

   ```
   python manage.py --port=7777
   ```
