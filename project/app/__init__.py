from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)
    project_root = Path(__file__).resolve().parent.parent
    database_path = project_root / "data" / "expenses.db"

    app.config.update(
        SECRET_KEY="dev-secret-key",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{database_path}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from app.controllers import main_bp
    from app.models import seed_database

    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()
        seed_database()

    return app
