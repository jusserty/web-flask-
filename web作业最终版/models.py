# 与model相关的定义都放到这里
from exts import db
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)
class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)
class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    #外键（类型要与外键保持一致，这里同一为Integer）
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))
     #绑定UserModel，并给usermodel添加反向引用questions，可以拿到user所有的questions
    author = db.relationship(UserModel,backref="questions")
class ware(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    warehouse = db.Column(db.String(100), nullable=False)
    accounts = db.Column(db.String(100), nullable=False)
