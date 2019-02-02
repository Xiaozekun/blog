from flask import Blueprint, render_template, request, current_app, url_for, flash, redirect
from flask_login import login_required, current_user

from blog.models import Post, Category, Comment
from blog.forms import AdminCommentForm, CommentForm
from blog.extensions import db

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page,
                                                                     per_page=current_app.config['BLOG_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('blog/index.html', posts=posts, pagination=pagination)


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/category.html', pagination=pagination, posts=posts, category=category)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.desc()).paginate(page, per_page=per_page)
    comments = pagination.items

    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['BLOG_EMAIL']
        form.site.data = url_for('.index')
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False
    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(author=author, site=site, email=email, body=body,
                          from_admin=from_admin, reviewed=reviewed, post=post)
        replied_id = request.args.get('reply')
        replied_comment = Comment.query.get_or_404(replied_id)
        comment.replied = replied_comment
        # TODO 发送邮件给被回复的人
        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:
            flash('Comment published.', 'success')
        else:
            flash('Thanks, your comment will be published after reviewed.', 'info')
            # TODO 发送邮件给管理员
        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, comments=comments, pagination=pagination, form=form)


@blog_bp.route('/reply_comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.post.can_comment:
        flash("Post can't comment.", 'warning')
        return redirect(url_for('.show_post', post_id=comment.post_id))
    return redirect(
        url_for('.show_post', author=comment.author, reply=comment_id, post_id=comment.post_id) + '#comment-form')
