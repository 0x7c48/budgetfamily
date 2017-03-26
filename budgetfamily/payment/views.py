# -*- coding: utf-8 -*-

"""
    payment.views
    ~~~~~~~~~~
"""

from flask_admin import BaseView, expose
from flask.ext.security import current_user
from flask.ext.admin.form.rules import FieldSet, Macro

from budgetfamily.core import base, mixins
from budgetfamily.core.rules import FormGroup, ReadOnly
from budgetfamily.auth.permissions import Action
from budgetfamily.payment.models import (Amount, ExchangeRate, 
    Salary, CashFlow, BankAccount, Deposit, Costs)  # Bank


class AmountAdmin(base.ModelView):
    model_class = Amount

    is_accessible = (Action.user_view_amount | Action.user_edit_amount | 
                     Action.user_create_amount | Action.user_delete_amount)
    can_edit      = property(Action.user_view_amount | Action.user_edit_amount)
    can_create    = property(Action.user_create_amount)
    can_delete    = property(Action.user_delete_amount)

    simple_list_pager = True
    page_size = 200

    #form_excluded_columns = ('source_amounts', 'compare_amounts', 'salary_amounts', 'cash_flow_amounts')
    column_hide_backrefs = True
    #form_rules = [ReadOnly('user')]

    def edit_form(self, obj=None):
        form = super(AmountAdmin, self).edit_form(obj)
        form.user.data = current_user
        return form


class ExchangeRateAdmin(base.ModelView):
    model_class = ExchangeRate
    edit_template = '1edit.html'

    is_accessible = (Action.user_view_amount | Action.user_edit_amount | 
                     Action.user_create_amount | Action.user_delete_amount)
    can_edit      = property(Action.user_view_amount | Action.user_edit_amount)
    can_create    = property(Action.user_create_amount)
    can_delete    = property(Action.user_delete_amount)

    simple_list_pager = True
    page_size = 200


class CashFlowAdmin(base.ModelView):
    model_class = CashFlow

    is_accessible = (Action.user_view_amount | Action.user_edit_amount | 
                     Action.user_create_amount | Action.user_delete_amount)
    can_edit      = property(Action.user_view_amount | Action.user_edit_amount)
    can_create    = property(Action.user_create_amount)
    can_delete    = property(Action.user_delete_amount)

    simple_list_pager = True
    page_size = 200


class BankAccountAdmin(base.ModelView):
    model_class = BankAccount

    is_accessible = (Action.user_view_amount | Action.user_edit_amount | 
                     Action.user_create_amount | Action.user_delete_amount)
    can_edit      = property(Action.user_view_amount | Action.user_edit_amount)
    can_create    = property(Action.user_create_amount)
    can_delete    = property(Action.user_delete_amount)

    simple_list_pager = True
    page_size = 200


# class BankAdmin(base.ModelView):
#     model_class = Bank

#     is_accessible = (Action.user_view_amount | Action.user_edit_amount | 
#                      Action.user_create_amount | Action.user_delete_amount)
#     can_edit      = property(Action.user_view_amount | Action.user_edit_amount)
#     can_create    = property(Action.user_create_amount)
#     can_delete    = property(Action.user_delete_amount)

#     simple_list_pager = True
#     page_size = 200


class DepositAdmin(base.ModelView):
    model_class = Deposit

    is_accessible = (Action.user_view_amount | Action.user_edit_amount | 
                     Action.user_create_amount | Action.user_delete_amount)
    can_edit      = property(Action.user_view_amount | Action.user_edit_amount)
    can_create    = property(Action.user_create_amount)
    can_delete    = property(Action.user_delete_amount)

    simple_list_pager = True
    page_size = 200


class CostsAdmin(base.ModelView):
    model_class = Costs

    is_accessible = (Action.user_view_amount | Action.user_edit_amount | 
                     Action.user_create_amount | Action.user_delete_amount)
    can_edit      = property(Action.user_view_amount | Action.user_edit_amount)
    can_create    = property(Action.user_create_amount)
    can_delete    = property(Action.user_delete_amount)

    simple_list_pager = True
    page_size = 200


class IncomeAdmin(base.ModelView):
    model_class = Costs

    simple_list_pager = True
    page_size = 200


############################
##  Control View
############################


class SalaryAdmin(base.ModelView):
    model_class = Salary

    is_accessible = (Action.user_view_amount | Action.user_edit_amount | 
                     Action.user_create_amount | Action.user_delete_amount)
    can_edit      = property(Action.user_view_amount | Action.user_edit_amount)
    can_create    = property(Action.user_create_amount)
    can_delete    = property(Action.user_delete_amount)

    simple_list_pager = True
    page_size = 200
    column_hide_backrefs = True

    form_rules = [
        ReadOnly('create_at'),
        FieldSet(('amount', ), u''),
        FormGroup('', """
                <a href="{{ url_for('amount.create_view', url=return_url) }}"
                onclick="return !window.open(this.href, 'Google', 'width=1000, height=500')"
                target="_blank">+++</a>
                """),
        ReadOnly('date_time'),
        ReadOnly('exchange_rate'),
        ReadOnly('description'),
    ]


class IncomeView(BaseView):
    @expose('/')
    def index(self):
        from flask_wtf import Form
        from wtforms.ext.appengine.db import model_form
        from budgetfamily.payment.models import Salary
        form = model_form(Salary, Form)
        return self.render('income_view.html', form=form)

class CostsView(BaseView):
    @expose('/')
    def index(self):
        return self.render("11")


class BalanceView(BaseView):
    @expose('/')
    def index(self):
        return self.render("11")


class MonthReportView(BaseView):
    @expose('/')
    def index(self):
        return self.render("11")


class YearReportView(BaseView):
    @expose('/')
    def index(self):
        return self.render("11")


class ExchangeRateView(BaseView):
    @expose('/')
    def index(self):
        return self.render("11")


class StockRateView(BaseView):
    @expose('/')
    def index(self):
        return self.render("11")


class DepositView(BaseView):
    @expose('/')
    def index(self):
        return self.render("11")


class CashFlowView(BaseView):
    @expose('/')
    def index(self):
        return self.render("11")


class BankAccountView(BaseView):
    @expose('/')
    def index(self):
        return self.render("11")


class BankBalanceView(BaseView):
    @expose('/')
    def index(self):
        return self.render("11")


class TaxesECBView(BaseView):
    @expose('/')
    def index(self):
        return self.render("11")


class TaxesEHView(BaseView):
    @expose('/')
    def index(self):
        return self.render("11")


class FutureIncomeView(BaseView):
    @expose('/')
    def index(self):
        return self.render("11")


class FutureCostsView(BaseView):
    @expose('/')
    def index(self):
        return self.render("11")
