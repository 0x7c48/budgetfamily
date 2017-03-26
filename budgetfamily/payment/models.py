# -*- coding: utf-8 -*-

"""
    payment.models
    ~~~~~~~~~~~
"""

import datetime
import itertools
import collections

from flask.ext.security import UserMixin, RoleMixin
from flask_security.utils import encrypt_password

from budgetfamily import db
from budgetfamily.auth.models import User


AmountOptions = collections.namedtuple(
    'AmountOptions',
    'currency, lang')


class AmountType(object):
    UAH = AmountOptions._make([u'uah', u'UA'])
    USD = AmountOptions._make([u'usd', u'USA'])

    @classmethod
    def choices(cls):
        return [cls.UAH.currency, cls.USD.currency]


class Amount(db.Model):
    __tablename__ = 'amount'

    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    value = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.Enum(*AmountType.choices(),
        name='amount_types'), default=AmountType.UAH)
    description = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, backref=db.backref('useramounts', lazy='joined'))

    def __unicode__(self):
        return u'{0} {1}'.format(self.value, self.currency)


class ExchangeRate(db.Model):
    __tablename__ = 'exchange_rate'
    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    name = db.Column(db.String(255))
    date_time = db.Column(db.DateTime, default=datetime.datetime.now)
    source_id = db.Column(db.Integer, db.ForeignKey(Amount.id))
    source = db.relationship(Amount, foreign_keys=source_id,
        backref=db.backref('source_amounts', lazy='joined'))
    compare_id = db.Column(db.Integer, db.ForeignKey(Amount.id))
    compare = db.relationship(Amount, foreign_keys=compare_id,
        backref=db.backref('compare_amounts', lazy='joined'))
    description = db.Column(db.String(500), nullable=True)

    # def __unicode__(self):
    #     return u'{0} {1} = {2} {3}'.format(self.source.value, self.compare.value,
    #         self.source.currency, self.compare.currency)


class Salary(db.Model):
    __tablename__ = 'salary'

    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    amount_id = db.Column(db.Integer, db.ForeignKey(Amount.id))
    amount = db.relationship(Amount, foreign_keys=amount_id, backref=db.backref('salary_amounts', lazy='joined'))
    date_time = db.Column(db.DateTime, default=datetime.datetime.now)
    exchange_rate_id = db.Column(db.Integer, db.ForeignKey(ExchangeRate.id))
    exchange_rate = db.relationship(ExchangeRate, foreign_keys=exchange_rate_id,
        backref=db.backref('exchange_rate_salaries', lazy='joined'))
    description = db.Column(db.String(500), nullable=True)


class CashFlow(db.Model):
    __tablename__ = 'cash_flow'

    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    name = db.Column(db.String(255))
    description = db.Column(db.String(500), nullable=True)
    amount_id = db.Column(db.Integer, db.ForeignKey(Amount.id))
    amount = db.relationship(Amount, backref=db.backref('cash_flow_amounts',
        lazy='joined'))


class BankAccount(db.Model):
    __tablename__ = 'bank_account'

    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    name = db.Column(db.String(255))
    description = db.Column(db.String(500), nullable=True)
    cash_flow_id = db.Column(db.Integer, db.ForeignKey(CashFlow.id))
    cash_flow = db.relationship(CashFlow, backref=db.backref('bank_account_cash_flows',
        lazy='joined'))


class Bank(db.Model):
    __tablename__ = 'bank'

    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    name = db.Column(db.String(255))
    bank_account_id = db.Column(db.Integer, db.ForeignKey(BankAccount.id))
    bank_account = db.relationship(BankAccount, backref=db.backref('bank_bank_accounts',
        lazy='joined'))
    description = db.Column(db.String(500), nullable=True)


class Deposit(db.Model):
    __tablename__ = 'deposit'
    
    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    name = db.Column(db.String(255))
    date_time = db.Column(db.DateTime, default=datetime.datetime.now)
    description = db.Column(db.String(500), nullable=True)
    cash_flow_id = db.Column(db.Integer, db.ForeignKey(CashFlow.id))
    cash_flow = db.relationship(CashFlow, backref=db.backref('deposit_flows',
        lazy='joined'))


class Costs(db.Model):
    __tablename__ = 'costs'

    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    cash_flow_id = db.Column(db.Integer, db.ForeignKey(CashFlow.id))
    cash_flow = db.relationship(CashFlow, backref=db.backref('costs_cash_flows',
        lazy='joined'))
    name = db.Column(db.String(255))
    description = db.Column(db.String(500), nullable=True)
