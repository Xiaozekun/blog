from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError, Email, URL, Optional

from blog.models import Category


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1,30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8,128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1,60)])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')
    category = SelectField('category', coerce=int, default=1)

    def __init__(self, *args, **kwargs):
        # 绝了
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.all()]


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1,30)])
    submit = SubmitField('Submit')

    # 自定义验证是否重复
    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')


class CommentForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,255), Email()])
    # site 可以为0,所以0~255
    site = StringField('Site', validators=[Optional(), URL(), Length(0,255)])
    author = StringField('Author', validators=[DataRequired(), Length(1,30)])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()