# -*- coding: utf-8 -*-

from apps import db

class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    author = db.Column(db.String(255))
    date_created = db.Column(db.DateTime(), default=db.func.now())
    univ_id = db.Column(db.Integer)
    photo = db.Column(db.String(255))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'))
    forum = db.relationship('Forum',
                              backref=db.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))
    photo = db.Column(db.String(255))
    author = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    content = db.Column(db.Text())
    date_created = db.Column(db.DateTime(), default=db.func.now())

class QnA(db.Model):
    __tablename__ = 'qna'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    author = db.Column(db.String(255))
    date_created = db.Column(db.DateTime(), default=db.func.now())
    univ_id = db.Column(db.Integer)
    photo = db.Column(db.String(255))

class QnAComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qna_id = db.Column(db.Integer, db.ForeignKey('qna.id'))
    qna = db.relationship('QnA',
                              backref=db.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))
    photo = db.Column(db.String(255))
    author = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    content = db.Column(db.Text())
    date_created = db.Column(db.DateTime(), default=db.func.now())

class Free(db.Model):
    __tablename__ = 'free'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    author = db.Column(db.String(255))
    date_created = db.Column(db.DateTime(), default=db.func.now())
    univ_id = db.Column(db.Integer)
    photo = db.Column(db.String(255))

class FreeComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    free_id = db.Column(db.Integer, db.ForeignKey('free.id'))
    free = db.relationship('Free',
                              backref=db.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))
    photo = db.Column(db.String(255))
    author = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    content = db.Column(db.Text())
    date_created = db.Column(db.DateTime(), default=db.func.now())

class Humor(db.Model):
    __tablename__ = 'humor'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    author = db.Column(db.String(255))
    date_created = db.Column(db.DateTime(), default=db.func.now())
    univ_id = db.Column(db.Integer)
    photo = db.Column(db.String(255))

class HumorComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    humor_id = db.Column(db.Integer, db.ForeignKey('humor.id'))
    humor = db.relationship('Humor',
                              backref=db.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))
    photo = db.Column(db.String(255))
    author = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    content = db.Column(db.Text())
    date_created = db.Column(db.DateTime(), default=db.func.now())

class FAQ(db.Model):
    __tablename__ = 'faq'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    author = db.Column(db.String(255))
    date_created = db.Column(db.DateTime(), default=db.func.now())
    univ_id = db.Column(db.Integer)
    photo = db.Column(db.String(255))

class FAQComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faq_id = db.Column(db.Integer, db.ForeignKey('faq.id'))
    faq = db.relationship('FAQ',
                              backref=db.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))
    photo = db.Column(db.String(255))
    author = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    content = db.Column(db.Text())
    date_created = db.Column(db.DateTime(), default=db.func.now())

class Notice(db.Model):
    __tablename__ = 'notice'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    author = db.Column(db.String(255))
    date_created = db.Column(db.DateTime(), default=db.func.now())
    univ_id = db.Column(db.Integer)
    photo = db.Column(db.String(255))

class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    author = db.Column(db.String(255))
    date_created = db.Column(db.DateTime(), default=db.func.now())
    univ_id = db.Column(db.Integer)
    photo = db.Column(db.String(255))


class BoardComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    board = db.relationship('Board',
                              backref=db.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))
    photo = db.Column(db.String(255))
    author = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    content = db.Column(db.Text())
    date_created = db.Column(db.DateTime(), default=db.func.now())

class Member(db.Model):
    email = db.Column(db.String(255), primary_key=True)
    level = db.Column(db.Integer, default=5) # forms에 립력 금지(회원가입시 입력 불가능하게...)
    pw = db.Column(db.String(255))
    univname = db.Column(db.String(255))
    avg_credit = db.Column(db.Integer)
    eng_score = db.Column(db.Integer)
    grade = db.Column(db.Integer)
    major = db.Column(db.String(255))
    name = db.Column(db.String(255))
    join_date = db.Column(db.DateTime(), default= db.func.now())

class K_Univ(db.Model):
    __tablename__ = 'k_univ'
    univ_id = db.Column(db.Integer, primary_key=True)
    univname = db.Column(db.String(255))

class I_Univ(db.Model):
    __tablename__ = 'i_univ'
    univ_id = db.Column(db.Integer, primary_key=True)
    univ_name= db.Column(db.String(255))
    nation = db.Column(db.String(255))
    state = db.Column(db.String(255), default="none")
    city = db.Column(db.String(255))
    avg_credit = db.Column(db.Integer)
    eng_score = db.Column(db.Integer)
    student = db.Column(db.Integer)
    tuition = db.Column(db.Integer) 
    cost = db.Column(db.Integer)
    house = db.Column(db.Integer)
    content = db.Column(db.Text())
    date_created = db.Column(db.DateTime(), default=db.func.now())

class R_Univ(db.Model):
    __tablename__ = 'r_univ'
    id = db.Column(db.Integer, primary_key=True)
    K_Univ_id = db.Column(db.Integer, db.ForeignKey('k_univ.univ_id'))
    k_univ = db.relationship('K_Univ',
                                backref=db.backref('r_univ', cascade='all, delete-orphan', lazy='dynamic'))
    I_Univ_id = db.Column(db.Integer, db.ForeignKey('i_univ.univ_id'))
    i_univ = db.relationship('I_Univ', backref=db.backref('r_univ', cascade='all, delete-orphan', lazy='dynamic'))
