from app import app    # from 'app' (package) import 'app' (variable)

@app.route('/')
@app.route('/index/')
def index():
    return "Hello, World!"

