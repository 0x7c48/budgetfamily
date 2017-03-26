# -*- coding: utf-8 -*-

"""
    payment.forms
    ~~~~~~~~~~
"""


from flask_wtf import Form
from wtforms.ext.appengine.db import model_form
from budgetfamily.payment.models import Salary


IncomeViewForm = model_form(Salary, Form)


class IncomeViewForm(Form):
    mobile_list = fields.TextAreaField(
        label=u'Список телефонных номеров',
        validators=[v.Required(), ],
        widget=defaults(widgets.TextArea(), rows=15))

    def __init__(self, *args, **kwargs):
        super(FraudForm, self).__init__(*args, **kwargs)
        self.clean_mobile_list = []
        self.error_mobile_list = []
