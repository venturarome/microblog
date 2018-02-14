from app import app, db
from app.models import User, Comment

# Create a shell context that adds the database instance and models to the shell session ($: flask shell)
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Comment': Comment}

