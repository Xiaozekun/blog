import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from blog.models import Admin, Category, Post, Comment
from blog.extensions import db

fake = Faker(locale='zh_CN')

def fake_admin():
    db.create_all()
    admin = Admin(
        username='admin',
        name='Xiaozekun',
        about='编程工程师',
        blog_title='我的BLOG',
        blog_sub_title='lihfts,hhhhhhh'
    )
    admin.set_password('1q2w3e4t5r')
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    category = Category(name='default')
    db.session.add(category)
    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def fake_posts(count=50):
    for i in  range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            timestamp=fake.date_time_this_year(),
            category= Category.query.get(random.randint(1, Category.query.count())),
            can_comment= random.randint(0,1)
        )
        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    for i in range(count):
        comment = Comment(
            email=fake.email(),
            site=fake.url(),
            author=fake.name(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count*0.1)
    for i in  range(salt):
        comment = Comment(
            email=fake.email(),
            site=fake.url(),
            author=fake.name(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

        comment = Comment(
            author='Xiaozekun',
            site='lihfts@club',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    for i in  range(salt):
        comment = Comment(
            email=fake.email(),
            site=fake.url(),
            author=fake.name(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count())),
            replied=Comment.query.get(random.randint(1, Comment.query.count()))
        )
        db.session.add(comment)
    db.session.commit()