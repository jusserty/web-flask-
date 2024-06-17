import wtforms
from flask_wtf import FlaskForm
from wtforms.validators import Email, EqualTo, Length
from models import UserModel, EmailCaptchaModel
from exts import db


class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致")])

    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册")

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或者验证码错误")
        else:
            db.session.delete(captcha_model)
            db.session.commit()


class RegistrationForm(FlaskForm):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])
#验证前端登录获取的数据是否满足要求
class QuestionForm(wtforms.Form):
#直接定义验证规则(这里不需要用户再传create_time、author_id，默认使用当前时间和当前用户即可)
   title = wtforms.StringField(validators=[Length(min=3,max=100,message="标题格式错误")])
   content = wtforms.StringField(validators=[Length(min=3,message="内容格式错误")]) #长度不限制