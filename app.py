import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def app_factory(testing=False):
    app = Flask(__name__)

    APP_ENV = os.environ.get("FLASK_ENV", "PRODUCTION")

    if APP_ENV == 'PRODUCTION':
        app.config.from_object('instance.config.ProdConfig')
    elif testing:
        app.config.from_object('instance.config.TestConfig')
    else:
        app.config.from_object('instance.config.DevConfig')

    # Models
    from models import User

    # Bps
    from routes import user_blueprint

    app.register_blueprint(user_blueprint)

    jwt = JWTManager()

    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    jwt.init_app(app=app)

    return app
