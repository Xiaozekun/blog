from datetime import datetime

from blog import db


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    # articles = db.relationship('Article', back_populates='author')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    posts = db.relationship('Post', back_populates='category')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True,)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # author = db.relationship('User', back_populates='articles')
    # author_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    category = db.relationship('Category', back_populates='posts')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    comments = db.relationship('Comment', back_poppulate='post', cascade='all')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    sites = db.Column(db.String(255))
    author = db.Column(db.String(30))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed = db.Column(db.Boolean, default=False)

    post = db.relationship('Post', back_poppulate='comments')
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    replied = db.relationship('Comment', back_populates='replies')
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'), remote_side=[id])

    replies = db.relationship('Comment', back_populates='replied', cascade='all')