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
from sleepypuppy.admin.puppyscript.models import Puppyscript


class Payload(db.Model):
    """
    Payload model contains the following parameters:

    payload = payload used in xss injection testing.
    url = url where payload is submitted to
    method = method of request to faciliate xss testing
    paramater = parameter which contains the payload
    notes = notes

    Payload provides primary key to Capture, which stores
    a xss capture.
    """
    __tablename__ = 'payloads'

    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(db.String(500))
    notes = db.Column(db.String(200))
    ordering = db.Column(db.String(200))
    # When payloads are deleted,
    # cascade the delete and remove associated captures
    # captures = db.relationship("Capture", cascade="all,delete", backref="payloads")
    # collection = db.relationship("GenericCollector", cascade="all,delete", backref="payloads")

    def as_dict(self):
        """
        Return JSON API object
        """
        puppyscripts = []
        for item in self.ordering.split(','):
            my_js = Puppyscript.query.filter_by(id=int(item)).first()
            puppyscripts.append(my_js.name)

        payload_dict = {
            "id": self.id,
            "puppyscripts": puppyscripts,
            "payload": self.payload,
            "notes": self.notes
        }

        return payload_dict

    def __repr__(self):
        return str(self.id)
