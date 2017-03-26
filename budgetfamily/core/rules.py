# -*- coding: utf-8 -*-

"""
    core.rules
    ~~~

"""


import jinja2

from flask.ext.admin import helpers
from flask.ext.admin.form import rules


class Template(rules.BaseRule):
    def __init__(self, template):
        super(rules.BaseRule, self).__init__()
        self.template = template

    def __call__(self, form, form_opts=None, field_args={}):
        context = helpers.get_render_ctx()
        tmpl = jinja2.Template(self.template)
        return jinja2.Markup(tmpl.render(context))

    @property
    def visible_fields(self):
        return []


def FormGroup(label, value):
    return Template(u'''
      <div class='form-group'>
        <div class='control-label col-md-2'><label>%s</label></div>
        <div class='col-md-10'>%s</div>
      </div>''' % (label, value))



class ReadOnly(rules.Macro):
    def __init__(self, field_name, render_field='macros.form_group'):
        self.field_name = field_name
        super(ReadOnly, self).__init__(render_field)

    def __call__(self, form, form_opts=None, field_args={}):
        ctx = helpers.get_render_ctx()

        if '.' not in self.field_name and self.field_name in form.data:
            value = form.data[self.field_name]
        else:
            model = self._resolve(ctx, 'model')

            try:
                value = reduce(lambda m, n: getattr(m, n) if m else None,
                               self.field_name.split('.'),
                               model)
            except AttributeError:
                raise ValueError('Model %s does not have field %s' %
                                 (model, self.field_name))

        view = self._resolve(ctx, 'admin_view')
        converter = view.model_form_converter(view.session, view)
        label = converter._get_label(self.field_name, {})

        params = {
            'label': label,
            'value': value
        }
        return super(ReadOnly, self).__call__(form, form_opts, params)
