#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    manage.py
    ~~~~~~
    Set of some useful management commands.
"""

import subprocess

from flask.ext.script import Shell, Manager
from flask.ext.security import utils

from budgetfamily import app, db, user_datastore
from budgetfamily.payment.models import User

manager = Manager(app)


@manager.command
def clean_pyc():
    """Removes all *.pyc files from the project folder"""
    clean_command = "find . -name *.pyc -delete".split()
    subprocess.call(clean_command)


@manager.command
def init_data():
    """Initial data for project"""


manager.add_command(
	'shell', Shell(make_context=lambda: {'app': app, 'db': db}))


@manager.command
def syncdb():
    db.create_all()
    create_superuser()


@manager.command
def create_superuser():
    user = user_datastore.create_user(
        email='test@gmail.com',
        password=utils.encrypt_password('test'),
        active=True,
        is_staff=True,
        is_superuser=True,
        username=u'test',
        first_name=u'test',
        last_name=u'test')
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
