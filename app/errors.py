from flask import render_template
from app import app, db

# 404: Page not found
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# 500: Internal server error (ie. database error)
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # Resets session to a clean state.
    return render_template('500.html'), 500

