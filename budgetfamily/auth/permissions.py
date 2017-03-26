# -*- coding: utf-8 -*-

"""
    permissions.py
    ~~~~~~~~~~~
"""


from flask.ext.security import current_user


class P(object):
    def __init__(self, *names):
        self.names = names

    def __repr__(self):
        return '<P: %s>' % ', '.join(self.names)

    def __call__(self, view=None):
        return (current_user.is_authenticated() and
                current_user.has_any_perm(*self.names))

    def __or__(self, other):
        return P(*set(self.names + other.names))


class Action(object):
    user_view_user = P('user_view_user')
    user_edit_user = P('user_edit_user')
    user_create_user = P('user_create_user')
    user_delete_user = P('user_delete_user')

    user_view_role = P('user_view_role')
    user_edit_role = P('user_edit_role')
    user_create_role = P('user_create_role')
    user_delete_role = P('user_delete_role')

    user_view_post = P('user_view_post')
    user_edit_post = P('user_edit_post')
    user_create_post = P('user_create_post')
    user_delete_post = P('user_delete_post')
    user_edit_template_post = P('user_edit_template_post')

    user_view_amount = P('user_view_amount')
    user_edit_amount = P('user_edit_amount')
    user_create_amount = P('user_create_amount')
    user_delete_amount = P('user_delete_amount')

    @classmethod
    def choices(cls):
        return [v.names[0] for k, v in cls.__dict__.items()
                if isinstance(v, P)]
