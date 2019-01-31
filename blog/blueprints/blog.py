from flask import Blueprint, render_template, request, current_app
from blog.models import Post
from flask_login import login_required


blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    page = request.args.get('page', 1 , type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page,
                                                                     per_page=current_app.config['BLOG_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('blog/index.html', posts=posts, pagination=pagination)
@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')

@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    return render_template('blog/category.html')

@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('blog/post.html', post=post)