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
from flask_wtf import Form
from flask import url_for, redirect, request
from flask.ext import admin, login
from flask.ext.admin import helpers, expose
from flask.ext.admin.contrib.sqla import ModelView
from wtforms import form, fields, validators
from sleepypuppy import db, bcrypt
from models import Administrator


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    """
    Class used to validate if a user is valid
    """
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        # Compare user and password to values in database
        user = self.get_admin()

        if user is None:
            raise validators.ValidationError('Invalid username or password')

        if not bcrypt.check_password_hash(user.password.encode('utf-8'), self.password.data):
            raise validators.ValidationError('Invalid username or password')

    def get_admin(self):
        # Retrieve the Administrator login
        return db.session.query(Administrator).filter_by(login=self.login.data).first()


class MyAdminIndexView(admin.AdminIndexView):
    """
    Exposes routes and mechanisms for application authentication
    """
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)

        if helpers.validate_form_on_submit(form):
            user = form.get_admin()
            login.login_user(user)

        if login.current_user.is_authenticated():
            return redirect(url_for('.index'))
        self._template_args['form'] = form

        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


class AdministratorView(ModelView):
    """
    Class overrides Model View from Flask Administrator.
    """
    # CSRF Protection
    form_base_class = Form

    # Check if user is authenticated
    def is_accessible(self):
        return login.current_user.is_authenticated()

    column_list = ('login', 'api_key')
    # Form overrides and validators for view
    form_columns = ('login', 'password', 'confirm')
    form_extra_fields = {
        'password': fields.PasswordField(
            'New Password',
            [
                validators.Required(),
                validators.EqualTo('confirm', message='Passwords must match')
            ]
        ),
        'confirm': fields.PasswordField('Repeat Password')
    }

    form_args = dict(
        login=dict(
            description="Login name for Sleepy Puppy dashboard",
            validators=[
                validators.required(),
                validators.Length(min=4, max=25)
            ]
        )
    )
