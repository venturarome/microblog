from flask import render_template
from app import app    # from 'app' (package) import 'app' (variable)

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


# INFO from here still not working.


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

