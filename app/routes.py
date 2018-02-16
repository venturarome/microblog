from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginTutoForm, RegistrationTutoForm, AddBlogEntryForm, AddEventForm, SampleForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

#=== Following tutorial
@app.route('/index/')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Index', posts=posts)


@app.route('/logintuto/', methods=['GET', 'POST'])
def tutologin():
    if current_user.is_authenticated:   # The current_user variable can be used at any time during the handling to obtain the user object that represents the client of the request. The value of this variable can be a user object from the database, or a special anonymous user object if the user did not log in yet.
        return redirect(url_for('index'))
    form = LoginTutoForm()
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
    return render_template('tutologin.html', title='Sign In', form=form)

@app.route('/logouttuto/')
def tutologout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/registertuto/', methods=['GET', 'POST'])
def tutoregister():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationTutoForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('tutologin'))
    return render_template('tutoregister.html', title='Register', form=form)




@app.route('/formtest/', methods=['GET', 'POST'])
def formtest():
    form = SampleForm()
    #if form.validate_on_submit():
        #flash('Login requested for user {}, remember_me={}'.format(
        #    form.username.data, form.remember_me.data)
        #)
        #return redirect(url_for('index'))
    return render_template('formtest.html', title='Test', form=form)






##### INFO from here still not working.

#=== Home Page
@app.route('/')
@app.route('/home/')
def home():
    # TODO add links not hardcoding, but using url_for, as explained in:
    # https://stackoverflow.com/questions/28207761/where-does-flask-look-for-image-files
    return render_template('home.html')

#=== About the author
@app.route('/about/')
def about():
    return render_template('about.html')

