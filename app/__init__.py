from flask import Flask
from app.module.dbModule import DB
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_socketio import SocketIO
from sqlalchemy import MetaData

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
mail = Mail()
socketIO = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    migrate.init_app(app, db)
    mail.init_app(app)
    socketIO.init_app(app)

    # db processing
    from . import models

    # Blue Prints
    from .views import main_views, auth_views, submit_views
    from app.test.index import test as test
    app.register_blueprint(main_views.bp)
    app.register_blueprint(test)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(submit_views.bp)
    return app
