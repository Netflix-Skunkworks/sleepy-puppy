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
import datetime
from sleepypuppy import db
from BeautifulSoup import BeautifulSoup as bs


class Capture(db.Model):
    """
    Capture model contains the following parameters:

    assessment = assessment name(s) assocaited with capture
    url = url where cross-site scripting was triggered
    referrer = referrer string of request
    cookies = any cookies not containing the HttpOnly flag from request
    user_agent = user-agent string
    payload = to be removed
    screenshot = screenshot identifier
    pub_date = Date with which the capature was recieved
    """
    __tablename__ = 'captures'

    id = db.Column(db.Integer, primary_key=True)
    assessment = db.Column(db.String(200))
    url = db.Column(db.Text(), unique=False)
    referrer = db.Column(db.Text(), unique=False)
    cookies = db.Column(db.Text(), unique=False)
    user_agent = db.Column(db.Text(), unique=False)
    payload = db.Column(db.Integer)
    screenshot = db.Column(db.String(20), unique=False)
    pub_date = db.Column(db.String(512), unique=False)
    dom = db.Column(db.Text(), unique=False)

    def as_dict(self):
        """Return Capture model as JSON object"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __init__(self, assessment, url, referrer, cookies, user_agent,
                 payload, screenshot, dom, pub_date=None):
        self.assessment = assessment
        self.url = url
        self.referrer = referrer
        self.cookies = cookies
        self.user_agent = user_agent
        self.payload = payload
        self.screenshot = screenshot
        self.dom = bs(dom).prettify()
        # Set datetime when a capture is recieved
        if pub_date is None:
            pub_date = str(datetime.datetime.now())
        self.pub_date = pub_date

    def __repr__(self):
        return '<Uri %r>' % self.url
