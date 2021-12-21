from flask import  Blueprint, render_template, request, flash, redirect, url_for
from flask.helpers import url_for
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from .models import Posts
from . import db


views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    posts = Posts.query.all()

    return render_template('homepage.html', user=current_user, posts=posts)

@views.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not content:
            flash('Post and title cannot be empty', category='error')
        if not title:
            flash('title cannot be empty', category='error')
        else:
            post = Posts(title=title, content=content, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category="success")
            return redirect(url_for('views.home'))
        

    return render_template("create_post.html", user=current_user)

@views.route('/delete-post/<id>')
@login_required
def delete_post(id):
    post = Posts.query.filter_by(id=id).first()

    if not post:
        flash('Post does not exist', category='error')
    elif current_user.id != post.id:
        flash('You do not have permission to delete post', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category='success')

    return redirect(url_for('views.home'))