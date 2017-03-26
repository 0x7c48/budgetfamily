# -*- coding: utf-8 -*-

"""
    base.py
    ~~~~~~~~~~~
"""

from datetime import datetime

from flask import redirect, url_for
from flask.ext.admin.contrib import sqla

from budgetfamily.core import mixins, types


class ModelView(mixins.TemplateMixin, sqla.ModelView):

    model_form_converter = types.BFModelConverter

    column_type_formatters = {
        datetime: lambda view, v: v.strftime('%Y-%m-%d %H:%M')
    }

    def __init__(self, *args, **kwargs):
        if not self.model_class:
            raise Exception('%s has no model_class attribute' % type(self))
        super(ModelView, self).__init__(self.model_class, *args, **kwargs)

    def scaffold_sortable_columns(self):
        return dict(super(ModelView, self).scaffold_sortable_columns(),
                    id=self.model.id)

    def _show_missing_fields_warning(self, text):
        return

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

