# 与blog相关的路由与视图函数
from flask import Blueprint, render_template, request, redirect, session, url_for

from blueprints.forms import QuestionForm
from exts import db
from models import QuestionModel
from decorators import login_required

bp = Blueprint("qa", __name__,url_prefix="/")

@bp.route("/")
def index():
    return render_template("main.html")
@bp.route("/search")
def search():
  return "首页search"
@bp.route("/qa/public_question",methods=["GET","POST"])
@login_required #配置装饰器
def public_question():
    if request.method == "GET":
          return render_template("public_question.html")
    else:
       form = QuestionForm(request.form)
       if form.validate():
           title = form.title.data
           content = form.content.data
           question = QuestionModel(title=title,content=content)
           db.session.add(question)
           db.session.commit()
           return redirect("/")
       else:
          print(form.errors)
          return redirect(url_for("qa.public_question"))


