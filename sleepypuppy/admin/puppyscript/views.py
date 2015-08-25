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
from models import Puppyscript
from sleepypuppy.admin.payload.models import Payload
from flask.ext import login
from flask_wtf import Form
from sleepypuppy import db, app


class PuppyscriptView(ModelView):
    """
    ModelView override of Flask Admin for Puppyscripts.
    """
    # CSRF protection
    form_base_class = Form

    # Ensure user is authenticated
    def is_accessible(self):
        return login.current_user.is_authenticated()

    # No need to show the many/many relationship for payloads
    form_excluded_columns = ('payloads')

    # Excluding code from view
    column_exclude_list = ('code')

    def on_model_delete(self, model):
        try:
            payloads = Payload.query.all()
            for payload in payloads:
                if payload.ordering is not None:
                    payload.ordering = payload.ordering.replace(
                        str(model.id) + ",", "")
                    payload.ordering = payload.ordering.replace(
                        "," + str(model.id), "")
                    payload.ordering = payload.ordering.replace(
                        str(model.id), "")
                    db.session.add(payload)
                    db.session.commit()
        except Exception as err:
            app.logger.warn(err)

    def __init__(self, session, **kwargs):
        super(PuppyscriptView, self).__init__(Puppyscript, session, **kwargs)
