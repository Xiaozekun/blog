from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from slugify import slugify

from blog.extensions import db


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    posts = db.relationship('Post', back_populates='category')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    category = db.relationship('Category', back_populates='posts')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    comments = db.relationship('Comment', back_populates='post', cascade='all')

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.slug = slugify(self.title)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    site = db.Column(db.String(255))
    author = db.Column(db.String(30))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed = db.Column(db.Boolean, default=False)

    post = db.relationship('Post', back_populates='comments')
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    replies = db.relationship('Comment', back_populates='replied', cascade='all')