from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
    else:
        app.config.update(test_config)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False

    db.init_app(app)

    # Register the comment routes
    from .comments import comments_bp
    app.register_blueprint(comments_bp)

    # Register task routes
    from .tasks import tasks_bp
    app.register_blueprint(tasks_bp)

    with app.app_context():
        db.create_all()

    return app
