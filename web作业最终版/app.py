import datetime
from flask import request, render_template, g, session
from flask import Flask,send_from_directory
from flask_jwt_extended import JWTManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate
import os

import config
from exts import db,mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp

app = Flask(__name__)
app.config.from_object(config)
# db=SQLAlchemy(app)
db.init_app(app)
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)
mail.init_app(app)
Session(app)

migrate=Migrate(app,db)

@app.route('/load/<path:filename>')
def load_custom_html(filename):
    # 设置 templates 文件夹的路径
    templates_path = os.path.join(app.root_path, 'templates')
    # 使用 send_from_directory 来发送 templates 文件夹中的文件
    return send_from_directory(templates_path, filename)
@app.before_request
def my_before_request():
    userid=session.get('user_id')
    if userid:
        user=UserModel.query.get(userid)
        setattr(g,"user",user)
    else:
        setattr(g,"user",None)
@app.context_processor
def my_context_processor():
    return {"user":g.user}

if __name__ == '__main__':
    app.run(debug=True)
