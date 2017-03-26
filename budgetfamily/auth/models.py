# -*- coding: utf-8 -*-

"""
    auth.models
    ~~~~~~~~~~~
"""

import itertools
import datetime

from sqlalchemy.dialects.postgresql import ARRAY, JSON
from flask.ext.security import UserMixin, RoleMixin, current_user
from flask_security.utils import encrypt_password

from budgetfamily import db


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('auth_user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text())
    permissions = db.Column(ARRAY(db.Text(), dimensions=1))

    def __unicode__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'auth_user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255))
    active = db.Column('is_active', db.Boolean(), nullable=False, default=True)
    username = db.Column(db.String(128), nullable=False, default=' ')
    first_name = db.Column(db.String(30), nullable=False, default=' ')
    last_name = db.Column(db.String(30), nullable=False, default=' ')
    is_staff = db.Column(db.Boolean(), nullable=False, default=False)
    is_superuser = db.Column(db.Boolean(), nullable=False, default=False)
    last_login = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    roles = db.relationship(Role, secondary=roles_users,
                            backref=db.backref('users'))

    def __unicode__(self):
        return u'{0} {1}'.format(self.id, self.email)

    def has_any_perm(self, *perms):
        has = set(itertools.chain.from_iterable(
            role.permissions for role in self.roles))
        return self.is_superuser or has.intersection(perms)


class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    phone = db.Column(db.String(17))
    user = db.relationship(User, backref=db.backref('user_profile_users', lazy='joined'))

    def __unicode__(self):
        return unicode(self.id)


class UserModType(object):
    USER_MOD_TYPE = 'user_mod_type'

    @classmethod
    def choices(cls):
        return [cls.USER_MOD_TYPE, ]


class UserMod(db.Model):
    __tablename__ = 'user_mod'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    type = db.Column(db.Enum(*UserModType.choices(), name='user_mod_types'))
    value = db.Column(JSON, nullable=True)
    user = db.relationship(User, backref=db.backref('usermods', lazy='joined'))
