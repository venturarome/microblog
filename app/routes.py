from flask import render_template, flash, redirect, url_for
from app import app    # from 'app' (package) import 'app' (variable)
from app.forms import LoginTutoForm, AddBlogEntryForm, AddEventForm, SampleForm

#=== Following tutorial
@app.route('/index/')
def index():
    user = {'username': 'Ventura'}
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
    return render_template('index.html', title='Index', user=user, posts=posts)

@app.route('/logintuto/', methods=['GET', 'POST'])
def tutologin():
    form = LoginTutoForm()
    if form.validate_on_submit():	# WTForms Built-in method: returns False on 'GET' or if validators failed.
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data)
        )
        return redirect(url_for('index'))
    return render_template('tutologin.html', title='Sign In', form=form)



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

