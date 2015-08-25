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
from sleepypuppy import db
from sqlalchemy.orm import relationship
from sleepypuppy.admin.models import user_associations
from sleepypuppy.admin.assessment.models import Assessment


class User(db.Model):
    """
    User model contains the following parameters used for email notifications:

    email = email address to send capture notifications to.
    assessments = list of assessments the email address will recieve captures for.

    Has an association of assessments with users.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    assessments = relationship(Assessment, secondary=user_associations, backref="users")

    def __repr__(self):
        return self.email
