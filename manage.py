from flask_script import Manager
from app import create_app

import os
import unittest
import datetime

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import *


manager = Manager(create_app())

manager.add_command('db', MigrateCommand)

@manager.command
def create_admin():
    db.session.add(User(email="leap1568@gmail.com",
                        password=generate_password_hash("admin"),
                        student_name='장해웅',
                        student_number='201945115',
                        authority=True,
                        nickname='leaps',
                        authority_type=1, # admin
                        registered_on=datetime.datetime.now()
                        ))
    db.session.commit()

@manager.command
def remove_account(email):
    model = User.query.get_or_404(email)
    db.session.delete(model)
    db.session.commit()

@manager.command
def run():
    app.run(host="0.0.0.0", port=80, debug=True)

@manager.command
def test():
    print('hello world')

if __name__ == '__main__':
    manager.run()