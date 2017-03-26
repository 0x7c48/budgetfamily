# -*- coding: utf-8 -*-

"""
    auth.views
    ~~~~~~~~~~
"""

from werkzeug.datastructures import MultiDict
from wtforms import widgets
from flask import after_this_request, redirect, request, url_for
from flask.ext import login as flogin
from flask.ext.security.views import _render_json, _ctx, _security, _commit
from flask.ext.security.utils import (login_user, get_post_login_redirect,
                                      config_value)
from flask.ext.security.decorators import anonymous_user_required
from flask.ext.security.utils import encrypt_password
from flask.ext.security.forms import LoginForm
from flask.ext.admin.form.rules import FieldSet
from flask.ext.admin.form.fields import Select2TagsField

from budgetfamily import db
from budgetfamily.auth.permissions import Action
from budgetfamily.auth.models import Role, User
from budgetfamily.core.rules import ReadOnly
from budgetfamily.core import base


@anonymous_user_required
def flask_login():
    """Login view with custom form validation.
    Login into site like Admin user (is_staff) 
    and like Control user (only is_authenticated).
    """

    if request.json:
        form = LoginForm(MultiDict(request.json))
    else:
        form = LoginForm()

    if form.validate_on_submit():
        login_user(form.user, remember=form.remember.data)
        after_this_request(_commit)

        if not request.json:
            return redirect(get_post_login_redirect(form.next.data))

    if request.json:
        return _render_json(form, include_auth_token=True)

    return _security.render_template(config_value('LOGIN_USER_TEMPLATE'),
                                     login_user_form=form,
                                     **_ctx('login'))


class MultiChoiceField(Select2TagsField):
    def __init__(self, label=None, validators=None, choices=(), **kwargs):
        self.choices = choices
        kwargs.setdefault('save_as_list', True)
        super(MultiChoiceField, self).__init__(label, validators, **kwargs)


class MultiChoiceWidget(widgets.TextInput):
    '''ref: https://github.com/mrjoes/flask-admin/blob/master/flask_admin/form/widgets.py#L31'''
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-role', u'select2-choices')
        kwargs.setdefault('data-choices', ','.join(field.choices))
        return super(MultiChoiceWidget, self).__call__(field, **kwargs)


class UserAdmin(base.ModelView):
    model_class = User

    # is_accessible = Action.user_view_user | Action.user_edit_user
    # can_edit = property(Action.user_edit_user)

    # column_searchable_list = ('email', )
    column_filters = ('email',)
    column_list = ('email', 'active', 'is_staff',)
    column_labels = {
        'email': u'Емейл'
    }

    form_edit_rules = [
        FieldSet((ReadOnly('email'),),
                 u'Данные'),
        FieldSet(('active', 'is_staff', 'is_superuser'),
                 u'Свойства'),
        FieldSet(('roles', ),
                 u'Права'),
        # FieldSet(('usermods', ),
        #          u'Дополнительные данные')
    ]

    # inline_models = [UserMod]

    def __init__(self, model, name=None, category='User',
                 endpoint='User', url=None):
        super(UserAdmin, self).__init__(model, name, category, endpoint, url)

    def after_model_change(self, form, model, is_created):
        if is_created:
            model.password = encrypt_password(model.password)
            db.session.add(model)
            db.session.commit()

    def _show_missing_fields_warning(self, text):
        return


class RoleAdmin(base.ModelView):
    model_class = Role

    is_accessible = Action.user_view_role | Action.user_edit_role
    can_edit = property(Action.user_edit_role)

    form_edit_rules = [FieldSet(('name', 'description', 'permissions')),
                       FieldSet(('users', ))]
    form_extra_fields = {
        'permissions': MultiChoiceField(choices=Action.choices(),
                                        widget=MultiChoiceWidget())
    }

    form_ajax_refs = {
        'users': {
            'fields': ['email']
        }
    }
