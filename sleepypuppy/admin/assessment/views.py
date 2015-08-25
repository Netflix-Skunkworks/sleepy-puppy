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
from models import Assessment
from sleepypuppy.admin.payload.models import Payload
from sleepypuppy.admin.capture.models import Capture
from sleepypuppy.admin.collector.models import GenericCollector
from sleepypuppy.admin.access_log.models import AccessLog
from flask.ext import login
from flask_wtf import Form
from sleepypuppy import app, db
import collections
import os

#
# Utility processors for healing with Assessment view.
#


@app.context_processor
def utility_processor():
    def get_payloads():
        the_payloads = Payload.query.all()
        results = collections.OrderedDict()
        for i in the_payloads:
            results[i] = i.payload
        return results
    return dict(get_payloads=get_payloads)


@app.context_processor
def utility_processor2():
    def get_hostname():
        return app.config['HOSTNAME']
    return dict(get_hostname=get_hostname)


@app.context_processor
def utility_processor3():
    def get_captures(data_type):
        magic_string = ""
        magic_string += "{"
        the_assessments = Assessment.query.all()
        the_payloads = Payload.query.all()
        for the_assessment in the_assessments:
            magic_string += "\'" + str(the_assessment.id) + "': {"
            for the_payload in the_payloads:
                if data_type == "capture":
                    cap_count = Capture.query.filter_by(
                        assessment=the_assessment.name, payload=the_payload.id).count()
                if data_type == "collector":
                    cap_count = GenericCollector.query.filter_by(
                        assessment=the_assessment.name, payload=the_payload.id).count()
                if data_type == "access_log":
                    cap_count = AccessLog.query.filter_by(
                        assessment=the_assessment.name, payload=the_payload.id).count()
                magic_string += str(the_payload.id) + \
                    ":" + str(cap_count) + ","
            magic_string += "},"
        magic_string += "}"
        return magic_string
    return dict(get_captures=get_captures)


class AssessmentView(ModelView):

    """
    ModelView override of Flask Admin for Assessments.
    """
    # CSRF Protecdtion
    form_base_class = Form

    # Check if user is authenticated
    def is_accessible(self):
        return login.current_user.is_authenticated()

    list_template = 'assessment_list.html'

    # Only display form columns listed below
    form_columns = ['name', 'access_log_enabled', 'snooze', 'run_once']
    column_list = ['name', 'snooze', 'run_once', 'access_log_enabled']

    def delete_captures(self, assessment):
        """
        Remove captures and local captures upon assessment deletion
        """
        cascaded_captures = Capture.query.filter_by(
            assessment=assessment.name).all()

        for capture in cascaded_captures:
            try:
                os.remove("uploads/{}.png".format(capture.screenshot))
                os.remove(
                    "uploads/small_{}.png".format(capture.screenshot))
            except:
                pass
        try:
            # Cascade delete for Assessment
            Capture.query.filter_by(assessment=assessment.name).delete()
            AccessLog.query.filter_by(assessment=assessment.name).delete()
            GenericCollector.query.filter_by(assessment=assessment.name).delete()
        except Exception as err:
            app.logger.warn(err)

        try:
            db.session.commit()
        except Exception as err:
            app.logger.warn(err)

    on_model_delete = delete_captures

    form_args = dict(
        access_log_enabled=dict(
            description="Record requests to payloads regardless if \
            they executed to the 'Access Log' \
            table for any payload associated with this assessment. \
            Recommended if you think you may hit namespace\
            conflicts or issues running JS payloads in victim's browser"
        ),
        snooze=dict(
            description="Stop captures for this payload"
        ),
        run_once=dict(
            description="Only run capture once for this payload"
        )
    )

    column_formatters = dict(
        payloads=lambda v, c, m, p: [Payload.query.all()])

    def __init__(self, session, **kwargs):
        super(AssessmentView, self).__init__(Assessment, session, **kwargs)
