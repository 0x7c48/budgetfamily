# -*- coding: utf-8 -*-

"""
    auth.forms
    ~~~~~~~~~~
"""


from flask.ext.security.confirmable import requires_confirmation
from flask.ext.security.forms import LoginForm, _datastore

from flask.ext.security.utils import (
    get_message, verify_and_update_password as _verify_and_update_password)

from budgetfamily import app


def verify_and_update_password(password, user):
    """Compare Django password sha1.
    """
    if app.config['SECURITY_PASSWORD_HASH'] == 'sha1_crypt':
        from .django_auth import check_password
        verified = check_password(password, user.password)
        return verified
    else:
        return _verify_and_update_password(password, user)


class AdminLoginForm(LoginForm):
    # TODO: fix email.strip()
    def validate(self):
        if not super(AdminLoginForm, self).validate():
            return False

        if self.email.data.strip() == '':
            self.email.errors.append(get_message('EMAIL_NOT_PROVIDED')[0])
            return False

        if self.password.data.strip() == '':
            self.password.errors.append(get_message('PASSWORD_NOT_PROVIDED')[0])
            return False

        self.user = _datastore.get_user(self.email.data)

        if self.user is None:
            self.email.errors.append(get_message('USER_DOES_NOT_EXIST')[0])
            return False
        if not self.user.password:
            self.password.errors.append(get_message('PASSWORD_NOT_SET')[0])
            return False
        if not verify_and_update_password(self.password.data, self.user):
            self.password.errors.append(get_message('INVALID_PASSWORD')[0])
            return False
        if requires_confirmation(self.user):
            self.email.errors.append(get_message('CONFIRMATION_REQUIRED')[0])
            return False
        if not self.user.is_active():
            self.email.errors.append(get_message('DISABLED_ACCOUNT')[0])
            return False
        # Check for staff
        if not self.user.is_staff:
            self.email.errors.append('ACCESS_DENIED')
            return False
        return True
