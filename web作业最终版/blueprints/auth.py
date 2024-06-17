# 与用户授权相关的路由与视图函数
import os
import string
import random
from flask import Flask,Blueprint, render_template, redirect, request, jsonify, session, url_for, flash,send_file
from exts import mail, db
from functools import wraps
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash
from models import EmailCaptchaModel, UserModel, ware
from .forms import RegisterForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
bp = Blueprint('auth', __name__, url_prefix='/auth')
owner=' '

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
                return redirect(url_for("MainPage"))

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
            global owner
            owner = email
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="密码错误")
    else:
        return jsonify(success=False, message="邮箱未注册")

@bp.route("/MainPage", methods=['GET'])
def MainPage():
    print("Session data:", session)
    if 'user_id' in session:
        return render_template("j.html")
    return render_template("fail-login.html")



@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        result = form.validate()
        print(result)
        if result:
            print('1613513515313135135')
            email = request.form.get('email')
            password1 = request.form.get('password')
            password=generate_password_hash(password1)
            username=request.form.get('username')
            user = UserModel(email=email, password=password, username=username)
            db.session.add(user)
            db.session.commit()
            flash('注册成功，请登录。','success')
            return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))

@bp.route('/menu')
def menu():  # put application's code here
    return render_template("menu.html")

@bp.route("/captcha/email")
def get_email_captha():
    email = request.args.get('email')
    print(string.digits)
    print(string.digits * 4)
    source = string.digits * 4
    captcha = random.sample(source, 4)
    print(captcha)
    captcha = ''.join(captcha)
    message = Message(subject="apex登陆验证码", recipients=[email], body=f'验证码是:{captcha}')
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

@bp.route("/logout",methods=['POST'])
def logout():
    session.pop('user_id',None)
    return jsonify({'status': 'logged_out'})
#------------------------------------------------------------------------------------------------#
# 设置静态文件目录
@bp.route('/your-backend-endpoint', methods=['POST'])
def handle_button_click():
    # 获取请求体中的数据
    button_id = request.json.get('buttonId')
    address_mapping = {
        'purchaseButton': 'static/images/r99.png',
        'purchaseButton2': 'static/images/dianneng.png',
        'purchaseButton3': 'static/images/fuchou.jpg',
        'purchaseButton4': 'static/images/lieshou.png'
    }

    # 根据 button_id 获取对应的 address
    address = address_mapping.get(button_id)

    if address:
        # 创建 test 实例
        new_record =ware(warehouse=address,accounts=owner)
        # 添加到数据库会话
        db.session.add(new_record)

        try:
            # 提交会话中的所有更改
            db.session.commit()
            print('Address saved successfully:', address)
            return jsonify(message='Address saved successfully', buttonId=button_id, warehouse=address), 201
        except Exception as e:
            # 如果发生错误，回滚更改
            db.session.rollback()
            print('Error saving address:', e)
            return jsonify(message='Error saving address', error=str(e)), 500
    else:
        # 如果没有找到对应的 button_id，返回错误信息
        return jsonify(message='Invalid button ID'), 400


@bp.route('/get-images', methods=['GET'])
def get_images():
    # 查询数据库，获取所有图片的绝对地址
    addresses = ware.query.filter_by(accounts=owner).all()

    # 将所有图片地址转换为 URL，并添加到列表中
    image_urls = []
    for address in addresses:
        file_path = address.warehouse
        if os.path.isfile(file_path):
            image_urls.append('/auth/get-image?image_path=' +file_path)

    # 返回包含所有图片 URL 的 JSON 对象
    return jsonify(image_urls=image_urls)

@bp.route('/get-image', methods=['GET'])
def get_image():
    # 从请求中获取图片的绝对地址
    image_path = request.args.get('image_path')

    # 确保文件路径是有效的
    if not os.path.isfile(image_path):
        return jsonify(message='File does not exist'), 404

    # 发送图片文件
    return send_file(image_path, mimetype='image/png')


