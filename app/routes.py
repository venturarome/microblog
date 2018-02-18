from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, CommentForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Comment
from werkzeug.urls import url_parse
from datetime import datetime


@app.before_request
def before_request():
    # The @before_request decorator registers the decorated function to be executed right before every view function in the application.
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/index/', methods=['GET', 'POST'])
@login_required
def index():
    form = CommentForm()

    # Handle form submission (POST):
    if form.validate_on_submit():
        comment = Comment(body=form.comment.data, author=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment is now live!')
        return redirect(url_for('index'))  # It is a common practice to respond to a POST request generated by a web form submission with a redirect (Post/Redirect/Get pattern).

    # Display comments (GET):
    page = request.args.get('page', 1, type=int)
    comments = current_user.followed_comments().paginate(page, app.config['POSTS_PER_PAGE'], False) # The 'paginate()' method returns a Pagination object.
    next_url = url_for('index', page=comments.next_num) if comments.has_next else None
    prev_url = url_for('index', page=comments.prev_num) if comments.has_prev else None
    return render_template('index.html', title='Home Page', form=form, comments=comments.items,
        next_url=next_url, prev_url=prev_url)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:   # The current_user variable can be used at any time during the handling to obtain the user object that represents the client of the request. The value of this variable can be a user object from the database, or a special anonymous user object if the user did not log in yet.
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():	# WTForms Built-in method: returns False on 'GET' or if validators failed.
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)   # This function will register the user as logged in.
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':   # netloc refers to the website domain.
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>/')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    comments = user.comments.order_by(Comment.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=comments.next_num) if comments.has_next else None
    prev_url = url_for('user', username=user.username, page=comments.prev_num) if comments.has_prev else None
    return render_template('user.html', user=user, comments=comments.items,
        next_url=next_url, prev_url=prev_url)

@app.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editprofile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('editprofile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('editprofile.html', title='Edit Profile',
                           form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    comments = ( Comment.query.order_by(Comment.timestamp.desc()).
        paginate(page, app.config['POSTS_PER_PAGE'], False) )
    next_url = url_for('explore', page=comments.next_num) if comments.has_next else None
    prev_url = url_for('explore', page=comments.prev_num) if comments.has_prev else None
    return render_template('index.html', title='Explore', comments=comments.items,
        next_url=next_url, prev_url=prev_url)

