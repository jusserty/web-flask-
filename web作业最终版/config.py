# # 与项目配置相关的定义
#mysql所在主机ip
import pymysql
HOSTNAME = '127.0.0.1'
#mysql监听的端口号，默认3306
PORT = 3306
#连接mysql的用户名（自己的）
USERNAME = 'root'
#连接mysql的密码（自己的）
PASSWORD = 'meng123'
#mysql上的数据库名称(需要先创建完成)
DATABASE = 'database_blog'
#app.config中配置flask连接数据库配置
'mysql+[driver]://[USERNAME]:[PASSWORD]@[HOSTNAME]:[PORT]/[DATABASE]?charset=utf-8'
SQLALCHEMY_DATABASE_URI= f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'


MAIL_SERVER = 'smtp.qq.com'
MAIL_USE_SSL=True
MAIL_PORT ="465"
MAIL_USERNAME="3150742519@qq.com"
MAIL_PASSWORD="myopdluszmqxdcdc"
MAIL_DEFAULT_SENDER="3150742519@qq.com"

SECRET_KEY = 'DAFDSFSDGGdfafdasfw'
SESSION_TYPE = 'filesystem'