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
from flask import render_template
from flask.ext.login import login_required
from sleepypuppy import app
from capture.models import Capture
from payload.models import Payload

#
# This is legacy code, not really documented/used
#


@app.route('/admin/capture/<int:id>')
@login_required
def show_capture(id):
    """
    Return a specific capture record and render using capture template.
    """
    captured = Capture.query.filter_by(payload=id).all()
    payload_assessment = Payload.query.filter_by(id=id).first()
    return render_template(
        'admin/capture.html',
        captured=captured,
        payload_assessment=payload_assessment,
        HOSTNAME=app.config['HOSTNAME']
    )


@app.context_processor
def capture_facts():
    """
    Returns the total number of captures in the database.
    """
    return dict(
        total_captures=Capture.query.count()
    )


@app.route('/admin/payload/<int:id>')
@login_required
def show_payload(id):
    """
    Return a specific payload record and render using payload template.
    """
    payload = Payload.query.filter_by(id=id).first()
    if payload is None:
        return render_template(
            'admin/payload.html',
            HOSTNAME="Not Found",
            pl="",
            query_len="",
            attack="Not Found"
        )

    attack = payload.payload.replace("$1", "//{}/x?u={}".format(app.config['HOSTNAME'], str(payload.id)))
    return render_template(
        'admin/payload.html',
        HOSTNAME=app.config['HOSTNAME'],
        pl=payload,
        attack=attack
    )
