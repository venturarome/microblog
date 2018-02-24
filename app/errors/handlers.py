from flask import render_template
from app import db
from app.errors import bp

# 404: Page not found
@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

# 500: Internal server error (ie. database error)
@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()  # Resets session to a clean state.
    return render_template('errors/500.html'), 500

