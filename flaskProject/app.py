import datetime
from flask import Flask, request, render_template, g, session
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate

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

migrate=Migrate(app,db)

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
