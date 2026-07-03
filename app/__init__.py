import os
from flask import Flask, render_template
import config

def create_app():
    """Flask app factory with configuration and blueprint registration"""
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY

    # Initialize database tables on startup
    with app.app_context():
        from app.database import create_tables
        create_tables()

    # Register authentication blueprint
    from app.routes.authRoutes import bp as auth_bp
    app.register_blueprint(auth_bp)

    # Register task blueprint
    from app.routes.taskRoutes import bp_tasks
    app.register_blueprint(bp_tasks)

    # Error handlers
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("403.html"), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template("500.html"), 500

    return app