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
from flask.ext.admin.contrib.sqla import ModelView
from wtforms.fields import SelectField, TextAreaField
from models import AccessLog
from flask.ext import login
from flask_wtf import Form


class AccessLogView(ModelView):
    """
    ModelView override of Flask Admin for Access Logs.
    """
    # CSRF protection
    form_base_class = Form

    # Ensure user is authenticated
    def is_accessible(self):
        return login.current_user.is_authenticated()

    form_excluded_columns = ('captures', 'uid')

    column_filters = ('id', 'payload', 'assessment', 'ip_address', 'user_agent', 'referrer')

    # Disable unnneeded CRUD operations
    can_create = False
    can_edit = False

    # Make form use dropdown boxes, default text, required form elements
    form_overrides = dict(
        method=SelectField,
        notes=TextAreaField
    )

    # Column list
    column_list = (
        'pub_date',
        'assessment',
        'payload',
        'referrer',
        'user_agent',
        'ip_address'
    )

    def __init__(self, session, **kwargs):
        super(AccessLogView, self).__init__(AccessLog, session, **kwargs)
