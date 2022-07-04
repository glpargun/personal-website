from email.policy import default
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150), unique=True)
    surname = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False, unique=True)
    title = db.Column(db.String, nullable=False, unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    likes = db.relationship('Like', backref='post', passive_deletes=True)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    ipaddress = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)


class About(db.Model):
    id = db.Column(db.Integer, primary_key=True, default=1)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    header = db.Column(db.String, nullable=False, default='a')
    body = db.Column(db.String, nullable=False, default='a')
    profil_photo = db.Column(db.String, nullable=False, default='a')
    p1 = db.Column(db.String, nullable=False, default='a')
    p1_link = db.Column(db.String, nullable=False, default='a')
    p2 = db.Column(db.String, nullable=False, default='a')
    p2_link = db.Column(db.String, nullable=False, default='a')
    p3 = db.Column(db.String, nullable=False, default='a')
    p3_link  = db.Column(db.String, nullable=False, default='a')
    p4 = db.Column(db.String, nullable=False, default='a')
    p4_link = db.Column(db.String, nullable=False, default='a')
    p5 = db.Column(db.String, nullable=False, default='a')
    p5_link = db.Column(db.String, nullable=False, default='a')
    random_facts = db.Column(db.String, nullable=False, default='a')

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    photo = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    name = db.Column(db.String, nullable=True)
    mail = db.Column(db.String, nullable=True)
    message = db.Column(db.String, nullable=True)
    statu = db.Column(db.Integer, nullable=False)
    ipaddress = db.Column(db.Integer, nullable=False)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ipaddress = db.Column(db.Integer, nullable=False)
    visit = db.Column(db.DateTime(timezone=True), default=func.now())
    page = db.Column(db.String, nullable=True)
