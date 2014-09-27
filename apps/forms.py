# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    SelectField,
    TextAreaField
)
from wtforms import validators
from wtforms.fields.html5 import EmailField

class ArticleForm(Form):
    title = StringField(
        u'제목',
        [validators.data_required(u'제목을 입력하시기 바랍니다.')],
        description={'placeholder': u'제목을 입력하세요.'}
    )
    content = TextAreaField(
        u'내용',
        [validators.data_required(u'내용을 입력하시기 바랍니다.')],
        description={'placeholder': u'내용을 입력하세요.'}
    )
    author = StringField(
        u'작성자',
        [validators.data_required(u'이름을 입력하시기 바랍니다.')],
        description={'placeholder': u'이름을 입력하세요.'}
    )
    category = StringField(
        u'카테고리',
        [validators.data_required(u'카테고리를 입력하시기 바랍니다.')],
        description={'placeholder': u'카테고리를 입력하세요.'}
    )


class CommentForm(Form):
    content = StringField(
        u'내용',
        [validators.data_required(u'내용을 입력하시기 바랍니다.')],
        description={'placeholder': u'내용을 입력하세요.'}
    )
    author = StringField(
        u'작성자',
        [validators.data_required(u'이름을 입력하시기 바랍니다.')],
        description={'placeholder': u'이름을 입력하세요.'}
    )
    password = PasswordField(
        u'비밀번호',
        [validators.data_required(u'비밀번호를 입력하시기 바랍니다.')],
        description={'placeholder': u'비밀번호를 입력하세요.'}
    )
    email = EmailField(
        u'이메일',
        [validators.data_required(u'이메일을 입력하시기 바랍니다.')],
        description={'placeholder': u'이메일을 입력하세요.'}
    )
class ForumForm(Form):
    title = StringField(
        u'제목',
        [validators.data_required(u'제목을 입력하시기 바랍니다.')],
        description={'placeholder': u'제목을 입력하세요.'}
    )
    content = TextAreaField(
        u'내용',
        [validators.data_required(u'내용을 입력하시기 바랍니다.')],
        description={'placeholder': u'내용을 입력하세요.'}
    )
    author = StringField(
        u'작성자',
        [validators.data_required(u'이름을 입력하시기 바랍니다.')],
        description={'placeholder': u'이름을 입력하세요.'}
    )

class JoinForm(Form):
    name = StringField(
        u'이름',
        [validators.data_required(u'이름을 입력하시기 바랍니다.')],
        description={'placeholder': u'이름을 입력하세요.'})
    email = EmailField(
        u'이메일',
        [validators.data_required(u'이메일을 입력하시기 바랍니다.')],
        description={'placeholder': u'이메일을 입력하세요.'}
    )
    password = PasswordField(
        u'비밀번호',
        [validators.data_required(u'비밀번호를 입력하시기 바랍니다.'),
        validators.EqualTo('confirm_password', message=u'비밀번호가 일치하지 않습니다.')],
        description={'placeholder': u'비밀번호를 입력하세요.'}
    )
    confirm_password = PasswordField(
        u'비밀번호 확인',
        [validators.data_required(u'비밀번호를 다시 입력하시기 바랍니다.')],
        description={'placeholder': u'비밀번호를 다시 입력하세요.'}
    )
    univname = SelectField(
    u'대학교', choices=[('1', u'명지대학교'), ('2', u'경희대학교'), ('3', u'연세대학교'), ('4', u'한국외국어대학교'), ('5', u'고려대학교')])
    grade = SelectField(
    u'학년', choices=[('1', u'1학년'), ('2', u'2학년'), ('3', u'3학년'), ('4', u'4학년')])
    
    major = StringField(
        u'전공',
        [validators.data_required(u'전공을 입력하시기 바랍니다.')],
        description={'placeholder': u'전공을 입력하세요.'})

class LoginForm(Form):
    email = EmailField(
        u'이메일',
        [validators.data_required(u'이메일을 입력하시기 바랍니다.')],
        description={'placeholder': u'이메일을 입력하세요.'})
    password = PasswordField(
        u'비밀번호',
        [validators.data_required(u'비밀번호를 입력하시기 바랍니다.')],
        description={'placeholder': u'비밀번호를 입력하세요.'})