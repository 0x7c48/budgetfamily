# -*- coding: utf-8 -*-

"""
    __init__.py
    ~~~~~~~~~~~
"""

import os, os.path as op

from flask import Flask
from flask.ext import admin
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask_environments import Environments

import flask_admin


app = Flask(__name__)
env = Environments(app)

ROOT = os.path.dirname(__file__)
CONFIG_YAML = 'config.yaml'

if os.path.exists(op.join(ROOT, 'config.yaml')):
    env.from_yaml(op.join(ROOT, 'config.yaml'))

if hasattr(app.config, 'DEBUG_TOOLBAR') and app.config['DEBUG_TOOLBAR']:
    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension(app)


db = SQLAlchemy(app)


# Custom login.
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Must be defined upper setup flask-security."""
    from budgetfamily.auth.views import flask_login
    return flask_login()


# Setup flask-security.
from budgetfamily.auth.models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


from budgetfamily.core import views as core_views

# control Index page
control = admin.Admin(app,
    url='/admin',
    index_view=core_views.ControlIndexView(
        url='/admin', name=u'Бюджет'),
    name=u'admin',
    base_template='layout.html',
    template_mode='bootstrap3')

# Payment app
from budgetfamily.payment import views as payment_views

# Ведомость
control.add_view(payment_views.SalaryAdmin(
    db.session, name=u'З/П', category=u'Ведомость', endpoint='salary'))
control.add_view(payment_views.IncomeView(
    name=u'Доход', category=u'Ведомость', endpoint='income-view'))
control.add_view(payment_views.CostsView(
    name=u'Расход', category=u'Ведомость', endpoint='costs-view'))
control.add_view(payment_views.BalanceView(
    name=u'Баланс', category=u'Ведомость', endpoint='balance-view'))
# Отчет
control.add_view(payment_views.MonthReportView(
    name=u'За месяц', category=u'Отчет', endpoint='month-report'))
control.add_view(payment_views.YearReportView(
    name=u'За год', category=u'Отчет', endpoint='year-report'))
# Курс
control.add_view(payment_views.ExchangeRateView(
    name=u'Валют', category=u'Курс', endpoint='exchangerate-view'))
control.add_view(payment_views.StockRateView(
    name=u'Акций', category=u'Курс', endpoint='stockrate-view'))
# Банк
control.add_view(payment_views.BankAccountView(
    name=u'Счета', category=u'Банк', endpoint='bank-account-view'))
control.add_view(payment_views.DepositView(
    name=u'Депозит', category=u'Банк', endpoint='deposit-view'))
control.add_view(payment_views.CashFlowView(
    name=u'Движение средств', category=u'Банк', endpoint='cash-flow-view'))
control.add_view(payment_views.BankBalanceView(
    name=u'Баланс', category=u'Банк', endpoint='bank-balance-view'))
# Налоги
control.add_view(payment_views.TaxesECBView(
    name=u'ЕСВ', category=u'Налоги', endpoint='taxes-ecb-view'))
control.add_view(payment_views.TaxesEHView(
    name=u'ЕН', category=u'Налоги', endpoint='taxes-eh-view'))
# План
control.add_view(payment_views.FutureIncomeView(
    name=u'Моделирование дохода', category=u'План', endpoint='future-income-view'))
control.add_view(payment_views.FutureCostsView(
    name=u'Моделирование расхода', category=u'План', endpoint='future-costs-view'))


# Auth Admin app, TODO is_staf only!
from budgetfamily.auth import views as auth_views
control.add_view(auth_views.UserAdmin(
    db.session, category=u'Admin', endpoint='user'))
control.add_view(auth_views.RoleAdmin(
    db.session, category=u'Admin', endpoint='role'))
control.add_view(payment_views.AmountAdmin(
    db.session, name=u'Amount', category=u'Admin', endpoint='amount'))
control.add_view(payment_views.ExchangeRateAdmin(
    db.session, name=u'ExchangeRate', category=u'Admin', endpoint='exchangerate'))
control.add_view(payment_views.CashFlowAdmin(
    db.session, name=u'CashFlow', category=u'Admin', endpoint='cashflow'))
control.add_view(payment_views.BankAccountAdmin(
    db.session, name=u'BankAccount', category=u'Admin', endpoint='bankaccount'))
control.add_view(payment_views.DepositAdmin(
    db.session, name=u'Deposit', category=u'Admin', endpoint='deposit'))


# Clear sessions.
@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()
