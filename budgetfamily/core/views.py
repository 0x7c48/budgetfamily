# -*- coding: utf-8 -*-

"""
    core.views
    ~~~~~~~~~~
"""


import datetime
import uuid
import os, os.path as op

from jinja2 import Markup
from flask import request, redirect, url_for, send_from_directory, Response
from flask.ext import admin, login as flogin
from flask.ext.admin import expose, form

from budgetfamily import app
from budgetfamily.core.base import ModelView
from budgetfamily.core.rules import ReadOnly


# Image allowed formats.
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def defaults(fn, **defaults):
    def inner(*args, **kw):
        return fn(*args, **dict(defaults, **kw))
    return inner


def make_image_path(subdir, name):
    datetime_dir = datetime.datetime.now().strftime("%Y/%m/%w%M")
    dirpath = op.join(app.root_path, app.config['UPLOAD_PATH'],
                      subdir, datetime_dir)
    if not op.exists(dirpath):
        os.makedirs(dirpath)
    return op.join(dirpath, name), op.join(subdir, datetime_dir, name)


@app.route('/')
def index():
    return 'Index Page'


@app.route('/media/<path:filename>', endpoint='media')
def uploaded_file(filename):
    """Media url"""
    return send_from_directory(
        op.join(app.root_path, app.config['UPLOAD_PATH']), filename)


@app.route('/media/add', methods=['POST'])
def upload_file():
    token = request.headers.get('X-TOKEN')
    if token != app.config.get('X_TOKEN'):
        return Response('Invalid token', 401)

    if 'file' not in request.files:
        return Response('No file supplied', 400)

    file = request.files['file']
    ext = file.filename.rsplit('.', 1)[1]
    if ext not in ALLOWED_EXTENSIONS:
        return Response('Invalid file extension', 400)

    filename = uuid.uuid4().hex + '.' + ext
    subdir = request.args.get('subdir', 'bestprice')
    image_path, image_url = make_image_path(subdir, filename)
    file.save(image_path)
    return Response(image_url)


class ControlIndexView(admin.AdminIndexView):
    @expose('/')
    def index(self):
        if not flogin.current_user.is_authenticated():
            return redirect(url_for('login', is_staff=True))
        return super(ControlIndexView, self).index()
