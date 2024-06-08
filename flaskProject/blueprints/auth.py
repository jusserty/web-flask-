# 与用户授权相关的路由与视图函数
import string
import random
from flask import Blueprint, render_template, redirect, request, jsonify, session, url_for, flash
from exts import mail, db
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash
from models import EmailCaptchaModel, UserModel
from .forms import RegisterForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


# @bp.route('/login')
# def login():
#     return render_template("login.html")


# @bp.route("/check-email-existence", methods=['POST'])
# def check_email_existence():
#     email = request.json.get('email')
#     password = request.json.get('password')
#     user = UserModel.query.filter_by(email=email).first()
#     if  not user:
#         return jsonify({'exists': False})
#     else:
#         if check_password_hash(user.password, password):
#             session['user_id'] = user.id
#             return jsonify({'exists': True})
#         else:
#             return jsonify({'exists': False})

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = UserModel.query.filter_by(email=email).first()
        if not user:
            flash("邮箱在数据库中不存在，请重新登录")
            return redirect(url_for("auth.login"))
        else:
            if check_password_hash(user.password, password):
                session["user_id"] = user.id
                return redirect("/")
            else:
                flash("密码错误")
                return redirect(url_for("auth.login", messages=session.get('_flashes', [])))

    return render_template("login.html")

@bp.route("/check-email-existence", methods=['POST'])
def check():
    email = request.json.get('email')
    password = request.json.get('password')
    user = UserModel.query.filter_by(email=email).first()

    if user:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="密码错误")
    else:
        return jsonify(success=False, message="邮箱未注册")

@bp.route("/MainPage", methods=['GET','POST'])
def main():
   return render_template("j.html")



@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        result = form.validate()
        if result:
            email = form.email.data
            password = form.password.data
            user=UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库中不存在，请重新登陆")
                return redirect(url_for("auth.login"))
            else:
                if check_password_hash(user.password, password):
                    session["user_id"] = user.id
                    return redirect("/")
                else:
                    print("密码错误")
                    return redirect(url_for("auth.login"))

        else:
            print(form.errors)
            return redirect(url_for("auth.register"))


@bp.route("/captcha/email")
def get_email_captha():
    email = request.args.get('email')
    print(string.digits)
    print(string.digits * 4)
    source = string.digits * 4
    captcha = random.sample(source, 4)
    print(captcha)
    captcha = ''.join(captcha)
    message = Message(subject="博客验证码", recipients=[email], body=f'验证码是:{captcha}')
    mail.send(message)
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({'code': 200, 'message': '', "data": captcha})


@bp.route("/mail/test")
def mail_test():
    message = Message(subject="apex登陆验证", recipients=["3150742519@qq.com"], body="这是测试邮件")
    mail.send(message)
    return "邮件发送成功"
@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
