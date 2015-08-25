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
from sleepypuppy import db, bcrypt
from sqlalchemy import event
from os import urandom


class Administrator(db.Model):
    """
    Admin model contols how users autheticate to Sleepy Puppy
    The model also automatically generates API keys for administrators.

    login = account for authetication
    password = self explanatory
    api_key = 40 character urandom hex encoded string
    """

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80))
    password = db.Column(db.String(64))
    api_key = db.Column(db.String(80))

    # Integrate Admin model with Flask Login
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __init__(self, login="", password=""):
        self.login = login
        self.password = password
        self.api_key = urandom(40).encode('hex')

    # Required for administrative interface
    def __unicode__(self):
        return self.username


# Make sure to encrypt passwords before create and updates
@event.listens_for(Administrator, 'before_insert')
def receive_before_insert(mapper, connection, target):
    target.password = bcrypt.generate_password_hash(target.password)
    target.api_key = urandom(40).encode('hex')


@event.listens_for(Administrator, 'before_update')
def receive_before_update(mapper, connection, target):
    target.password = bcrypt.generate_password_hash(target.password)
    target.api_key = urandom(40).encode('hex')
