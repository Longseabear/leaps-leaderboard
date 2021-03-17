from flask import Flask
from app.module.dbModule import DB
import config

db = DB(config.SQLALCHEMY_DATABASE_URI)

def create_app():
    app = Flask(__name__)

    # bluprint...
    from app.main.index import main as main
    from app.test.index import test as test
    app.register_blueprint(main)
    app.register_blueprint(test)
    return app