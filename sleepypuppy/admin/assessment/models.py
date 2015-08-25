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


class Assessment(db.Model):
    """
    Assessemt model contains the following parameters:

    name = name of the assessment you are working on.
    payloads = payloads assocaited with the assessment
    """
    __tablename__ = 'assessments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    snooze = db.Column(db.Boolean)
    run_once = db.Column(db.Boolean)
    access_log_enabled = db.Column(db.Boolean)

    def as_dict(self):
        """Return Assessment model as JSON object"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return str(self.name)
