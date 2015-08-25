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
from sleepypuppy import db, app
from sleepypuppy.admin.models import taxonomy
from flask import render_template_string


class Puppyscript(db.Model):

    """
    Puppyscript model contains the following parameters:

    name = name of javascriopt file.
    code = code that will be executed when a sleepy puppy payload is executed
    notes = notes

    Puppyscript is many to many with payload.
    """
    __tablename__ = 'puppyscript'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    code = db.Column(db.Text(), nullable=False)
    notes = db.Column(db.String(500))
    payloads = db.relationship(
        "Payload", backref='puppyscript', secondary=taxonomy)

    def show_puppyscript_ids(self):
        """
        Print puppyscripts as a list of Puppyscript ids.
        """
        return [i.id for i in self.Puppyscripts]

    def show_puppyscript_names(self):
        """
        Print puppyscripts as a string of Puppyscript ids.
        """
        return ','.join(
            [i.name for i in self.Puppyscripts]
        )

    def as_dict(self, payload=1, assessment=1):
        """
        Return Assessment model as JSON object

        If you need to expose addtional variables to your Puppyscript
        templates, this is the place to do it.
        """

        js_dict = {}
        js_dict['name'] = self.name
        js_dict['code'] = render_template_string(self.code,
                                                 hostname=app.config[
                                                     'CALLBACK_HOSTNAME'],
                                                 callback_protocol=app.config.get(
                                                     'CALLBACK_PROTOCOL', 'https'),
                                                 payload=payload, assessment=assessment)
        return js_dict

    def __repr__(self):
        return str(self.name)
