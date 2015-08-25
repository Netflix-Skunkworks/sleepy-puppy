#     Copyright 2015 Netflix, Inc.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
import os
from sleepypuppy import app, db
from flask.ext.admin.contrib.sqla import ModelView
from wtforms import validators
from wtforms.fields import SelectField, TextAreaField, SelectMultipleField
from wtforms.widgets import TextInput
from flask.ext.admin._compat import text_type
from sleepypuppy.admin.puppyscript.models import Puppyscript
from sleepypuppy.admin.capture.models import Capture
from models import Payload
from flask.ext import login
from flask_wtf import Form


class Select2MultipleWidget(TextInput):
    """
    (...)

    By default, the `_value()` method will be called upon the associated field
    to provide the ``value=`` HTML attribute.
    """

    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-choices', self.json_choices(field))
        return super(Select2MultipleWidget, self).__call__(field, **kwargs)

    @staticmethod
    def json_choices(field):
        objects = ('{{"id": {}, "text": "{}"}}'.format(*c)
                   for c in field.iter_choices())
        return '[' + ','.join(objects) + ']'


class Select2MultipleField(SelectMultipleField):
    """
        `Select2 <https://github.com/ivaynberg/select2>`_ styled select widget.

        You must include select2.js, form.js and select2 stylesheet for it to
        work.

        This is a slightly altered derivation of the original Select2Field.
    """
    widget = Select2MultipleWidget()

    def __init__(self, label=None, validators=None, coerce=text_type,
                 choices=None, allow_blank=False, blank_text=None, **kwargs):
        super(Select2MultipleField, self).__init__(
            label, validators, coerce, choices, **kwargs
        )
        self.allow_blank = allow_blank
        self.blank_text = blank_text or ' '
        self.choices = db.session.query(Puppyscript.id, Puppyscript.name).all()

    def iter_choices(self):
        # moved the query here so it updates
        choices = db.session.query(Puppyscript.id, Puppyscript.name).all()
        if self.allow_blank:
            yield (u'__None', self.blank_text, self.data is [])

        for value, label in choices:
            yield (value, label, self.coerce(value) in self.data)

    def process_data(self, value):
        if not value:
            self.data = []
        else:
            try:
                self.data = []
                for v in value:
                    self.data.append(self.coerce(v[0]))
            except (ValueError, TypeError):
                self.data = []

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == '__None':
                self.data = []
            else:
                try:
                    self.data = []
                    for value in valuelist[0].split(','):
                        self.data.append(self.coerce(value))
                except ValueError:
                    raise ValueError(
                        self.gettext(u'Invalid: Please set a Puppyscript for this payload {}'.format(value)))

    def pre_validate(self, form):
        if self.allow_blank and self.data is []:
            return

        super(Select2MultipleField, self).pre_validate(form)

    def _value(self):
        return ','.join(map(str, self.data))


class PayloadView(ModelView):
    """
    ModelView override of Flask Admin for Payloads.
    """
    # CSRF protection
    form_base_class = Form

    # Ensure user is authenticated
    def is_accessible(self):
        return login.current_user.is_authenticated()

    def on_form_prefill(self, form, id):
        # help order things in the right way.
        to_process = self.session.query(
            Payload.ordering).filter(Payload.id == id).first()
        if to_process[0]:
            form.puppyscript_list.process_data(to_process[0].split(','))

    # Custom templates for listing models
    list_template = 'payload_list.html'

    hostname = app.config['HOSTNAME']

    def on_model_change(self, form, model, is_created=False):
        try:
            model.ordering = ','.join(str(v) for v in form.puppyscript_list.data)
            db.session.add(model)
            db.session.commit()
        except Exception as err:
            app.logger.warn(err)

    # Method to cascade delete screenshots when removing a payload
    def delete_screenshots(self, model):
        cascaded_captures = Capture.query.filter_by(payload=model.id).all()
        for capture in cascaded_captures:
            try:
                os.remove("uploads/{}.png".format(capture.screenshot))
                os.remove("uploads/small_{}.png".format(capture.screenshot))
            except:
                pass
    on_model_delete = delete_screenshots

    # Column tweaks
    column_list = (
        'id',
        'payload',
        'puppyscripts',
        'notes'
    )

    column_sortable_list = (
        'id',
        'payload',
    )

    column_filters = (
        'id',
        'payload',
    )

    form_excluded_columns = ('captures', 'uid')
    form_columns = ('puppyscript_list',
                    'payload',
                    'notes')

    # Check if payload has associated captures, and format column if found
    # Format payload string to include hostname
    column_formatters = dict(
        puppyscripts=lambda v, c, m, p: [Puppyscript.query.filter_by(id=thing).first(
        ) for thing in Payload.query.filter_by(id=m.id).first().ordering.split(',')]
        if Payload.query.filter_by(id=m.id).first().ordering is not None or "" else "Default"
    )

    # Extra fields
    # 'puppyscript_list' name chosen to avoid name conflict
    form_extra_fields = {
        'puppyscript_list': Select2MultipleField(
            'Puppyscripts',
            coerce=int),
    }

    # Make form use dropdown boxes, default text, required form elements
    form_overrides = dict(
        method=SelectField,
        notes=TextAreaField
    )

    form_args = dict(
        payload=dict(
            description="Use $1 as a placeholder for the Puppyscript URL.",
            default="<script src=$1></script>",
            validators=[validators.required()]
        ),
        puppyscript_list=dict(
            description="Stuff.",
            label="Puppyscripts",
            validators=[validators.required()]
        )
    )

    def __init__(self, session, **kwargs):
        super(PayloadView, self).__init__(Payload, session, **kwargs)
