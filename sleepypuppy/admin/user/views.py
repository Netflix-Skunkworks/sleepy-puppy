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
from flask.ext import login
from flask_wtf import Form
from wtforms import validators
from models import User


class UserView(ModelView):
    """
    ModelView override of Flask Admin for Users.
    """
    # CSRF protection
    form_base_class = Form

    # Ensure user is authenticated
    def is_accessible(self):
        return login.current_user.is_authenticated()

    # Column tweaks
    column_list = ('email', 'assessments')
    column_labels = dict(email='Email Address', assessments='Assessments')

    # Form tweaks and validations
    form_args = dict(
        email=dict(
            description='Enter email address to recieve notifications when captures are recieved',
            validators=[validators.required(), validators.email()]
        ),
        assessments=dict(
            description='Subscribe to assessments to recieve notifications',
            validators=[validators.required()]
        )
    )

    def __init__(self, session, **kwargs):
        super(UserView, self).__init__(User, session, **kwargs)
