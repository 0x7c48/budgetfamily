# -*- coding: utf-8 -*-

"""
    base.py
    ~~~~~~~~~~~
"""


import json
import wtforms

from sqlalchemy import types
from dateutil import tz
from flask_admin.model.form import converts
from flask_admin.contrib.sqla.form import AdminModelConverter


class attrdict(dict):
    def __setattr__(self, key, value):
        self[key] = value


class JSONField(wtforms.fields.TextAreaField):
    def _value(self):
        return json.dumps(self.data) if self.data is not None else ''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = json.loads(valuelist[0])


class DynamicJsonForm(wtforms.Form):
    def __init__(self, formdata=None, obj=None, prefix='', data=None, meta=None, **kwargs):
        self._unbound_fields = []
        for key in kwargs:
            self._unbound_fields.append((key, wtforms.StringField(key)))
        super(DynamicJsonForm, self).__init__(formdata=formdata, obj=obj,
                                              prefix=prefix, data=data,
                                              meta=meta, **kwargs)


class COWFormField(wtforms.FormField):
    def populate_obj(self, obj, name):
        candidate = getattr(obj, name, None)
        if candidate is None:
            raise TypeError('Cannot find candidate')

        copy = attrdict(candidate)
        self.form.populate_obj(copy)
        setattr(obj, name, copy)


class UTCDateTime(types.TypeDecorator):
    '''Для тех полей, у которых в базе нет TZ, и они там хранятся как UTC
    '''

    impl = types.DateTime

    def process_bind_param(self, value, engine):
        if value is not None:
            return (value
                    .replace(tzinfo=tz.tzlocal())
                    .astimezone(tz.tzutc())
                    .replace(tzinfo=None))

    def process_result_value(self, value, engine):
        if value is not None:
            return (value
                    .replace(tzinfo=tz.tzutc())
                    .astimezone(tz.tzlocal())
                    .replace(tzinfo=None))


class LocalDateTime(types.TypeDecorator):
    '''Для тех полей, у которых в базе есть TZ, и они там хранятся как локальное
    время
    '''

    impl = types.DateTime

    def process_bind_param(self, value, engine):
        if value is not None:
            return value.replace(tzinfo=tz.tzlocal())

    def process_result_value(self, value, engine):
        if value is not None:
            return value.replace(tzinfo=None)


class BFModelConverter(AdminModelConverter):
    @converts('budgetfamily.core.types.UTCDateTime',
              'budgetfamily.core.types.LocalDateTime')
    def convert_mk_datetime(self, field_args, **extra):
        return self.convert_datetime(field_args, **extra)

    @converts('JSON')
    def convert_mk_json(self, field_args, **extra):
        return JSONField(**field_args)
