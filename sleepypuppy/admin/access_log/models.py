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
import datetime


class AccessLog(db.Model):
    """
    Access Log records GET requests to payloads.  This can be helpful
    for payloads that are not executing due to namespace conflicts, client
    side controls, or other unexpected issues.
    """

    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(db.Integer())
    assessment = db.Column(db.String(512))
    pub_date = db.Column(db.String(512), unique=False)
    referrer = db.Column(db.String(1024))
    user_agent = db.Column(db.String(512))
    ip_address = db.Column(db.String(80))

    def __init__(self, payload, assessment, referrer, user_agent, ip_address, pub_date=None):
        self.payload = payload
        self.assessment = assessment
        self.referrer = referrer
        self.user_agent = user_agent
        self.ip_address = ip_address
        if pub_date is None:
            pub_date = str(datetime.datetime.now())
        self.pub_date = pub_date

    def as_dict(self):
        """Return Access Log model as JSON object"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
