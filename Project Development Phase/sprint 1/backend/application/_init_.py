import ibm_db_sa
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import CONFIG_OBJECT_NAME

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(CONFIG_OBJECT_NAME)
    db.init_app(app)

    from application.auth.routes import auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix=app.config['API_VERSION_PREFIX'])

    with app.app_context():
        db.create_all()

    return app
