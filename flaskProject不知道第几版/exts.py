# SQLAIchemy对象定义到这里
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
"""
解决循环引用问题:这里只初始化SQLAlchemy，不与app进行绑定
"""
db = SQLAlchemy()
mail=Mail()